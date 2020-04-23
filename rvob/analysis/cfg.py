from collections import deque
from enum import Enum, auto
from itertools import count, chain
from typing import Iterator, FrozenSet

from networkx import DiGraph, simple_cycles, restricted_view, all_simple_paths

from rep.base import Instruction, Directive, ASMLine, to_line_iterator
from rep.fragments import Source, FragmentView
from rvob.structures import jump_ops, JumpType


class Transition(Enum):
    """A type of transition in a CFG."""

    # Sequential: PC advances into another labeled block
    SEQ = auto()
    # U-Jump: a simple local unconditional jump
    U_JUMP = auto()
    # C-Jump: a simple local conditional jump
    C_JUMP = auto()
    # Call: non-local jump to an internal or external procedure
    CALL = auto()
    # Return: return jump from a call
    RETURN = auto()


def build_cfg(src: Source, entry_point: str = "main") -> DiGraph:
    """
    Builds the CFG of the supplied assembly code, starting from the specified entry point.
    
    The entry point consists of a valid label pointing to what will be considered by the algorithm as the first
    instruction executed by a caller.
    The graph is built through a recursive DFS algorithm that follows the control flow.

    The resulting graph's nodes either contain a reference to a view, through the node attribute `block`, which
    represents the block of serial instructions associated with the node, or an `external` flag, signifying that the
    referenced code is external to the analyzed code.
    Nodes representing internal code have an incremental ID, while the external ones are uniquely identified through
    their symbol (aka procedure identifier).

    Nodes are connected through unweighted edges bearing a `kind` attribute, which describes the type of transition that
    that edge represents.

    :param src: the assembler source to be analyzed
    :param entry_point: the entry point from which the execution flow will be followed
    :return: a directed graph representing the CFG of the analyzed code
    :raise ValueError: when the entry point couldn't be found
    """

    def _explorer(start_line: int, __ret_stack__: deque):
        # Detect if there's a loop and eventually return the ancestor's ID to the caller
        if start_line in ancestors:
            return ancestors[start_line]

        # Instantiate an iterator that scans the source, ignoring directives
        line_supplier = filter(lambda s: isinstance(s.statement, Instruction),
                               to_line_iterator(src.iter(start_line), start_line))
        # Generate node ID for the root of the local subtree
        rid = next(id_sup)

        # Variable for keeping track of the previous line, in case we need to reference it
        previous_line = None

        for line in line_supplier:
            if len(line.statement.labels) != 0 and line.number != start_line:
                # TODO maybe we can make this iterative?
                # We stepped inside a new contiguous block: build the node for the previous block and relay
                cfg.add_node(rid, block=FragmentView(src, start_line, line.number, start_line))
                ancestors[start_line] = rid
                cfg.add_edge(rid, _explorer(line.number, __ret_stack__), kind=Transition.SEQ)
                break
            elif line.statement.opcode in jump_ops:
                # Create node
                cfg.add_node(rid, block=FragmentView(src, start_line, line.number + 1, start_line))
                ancestors[start_line] = rid

                if jump_ops[line.statement.opcode] == JumpType.U:
                    # Unconditional jump: resolve destination and relay-call explorer there
                    cfg.add_edge(rid,
                                 _explorer(label_dict[line.statement.immediate.symbol], __ret_stack__),
                                 kind=Transition.U_JUMP)
                    break
                elif jump_ops[line.statement.opcode] == JumpType.F:
                    # Function call: start by resolving destination
                    target = line.statement.immediate.symbol
                    # TODO find a way to modularize things so that this jump resolution can be moved out of its nest
                    try:
                        dst = label_dict[target]
                        # Update the return address
                        ret_stack.append(next(line_supplier).number)
                        # Set the current node as ancestor for the recursive explorer
                        home = rid
                        # Set transition type to CALL
                        tran_type = Transition.CALL
                    except KeyError:
                        # Calling an external function: add an edge to the external code node.
                        # The external node is uniquely identified by a call ID, so that client code of the graph can
                        # follow the execution flow among calls to the same external procedures.
                        call_id = target + str(next(id_sup))
                        cfg.add_node(call_id, external=True)
                        cfg.add_edge(rid, call_id, kind=Transition.CALL)

                        # Set the following line as destination
                        dst = next(line_supplier).number
                        # Set the external node as ancestor for the recursive explorer
                        home = call_id
                        # Set the the type of the transition from the external code back to us as RETURN
                        tran_type = Transition.RETURN

                    # Perform the actual recursive call
                    cfg.add_edge(home, _explorer(dst, __ret_stack__), kind=tran_type)
                    break
                elif jump_ops[line.statement.opcode] == JumpType.C:
                    # Conditional jump: launch two explorers, one at the jump's target and one at the following line
                    cfg.add_edge(rid, _explorer(next(line_supplier).number, __ret_stack__), kind=Transition.SEQ)
                    # The second explorer needs a copy of the return stack, since it may encounter another return jump
                    cfg.add_edge(rid,
                                 _explorer(label_dict[line.statement.immediate.symbol],
                                           __ret_stack__.copy()),
                                 kind=Transition.C_JUMP)
                    break
                elif jump_ops[line.statement.opcode] == JumpType.R:
                    # Procedure return: close the edge on the return address by invoking an explorer there
                    cfg.add_edge(rid, _explorer(__ret_stack__.pop(), __ret_stack__), kind=Transition.RETURN)
                    break
                else:
                    raise LookupError("Unrecognized jump type")

            previous_line = line.number
        else:
            cfg.add_node(rid, block=FragmentView(src, start_line, previous_line + 1, start_line))

        return rid

    # Generate the dictionary containing label mappings
    label_dict = src.get_labels()

    # Instantiate the node id supplier
    id_sup = count()

    # Instantiate an empty di-graph for hosting the CFG
    cfg = DiGraph()

    # Initialize the dictionary mapping blocks' initial lines to nodes
    ancestors = {}

    # Initialize the graph with a special root node
    root_id = next(id_sup)
    cfg.add_node(root_id, external=True)
    ancestors[-1] = root_id

    # Initialize the return stack
    ret_stack = deque()
    ret_stack.append(-1)

    # Call the explorer on the entry point and append the resulting graph to the root node
    try:
        child_id = _explorer(label_dict[entry_point], ret_stack)
    except KeyError:
        raise ValueError("Entry point [" + entry_point + "] not found")

    cfg.add_edge(root_id, child_id, kind=Transition.U_JUMP)

    return cfg


def get_stepper(cfg: DiGraph, entry_pnt: int) -> Iterator[ASMLine]:
    """
    Step execution through the CFG.

    Given a CFG and an optional starting point (entry-point), generates an iterator that follows the program's execution
    flow.

    When confronted by the bifurcating edges of a conditional branch situation, callers can `.send()` the condition's
    truth value in order to select the branch to follow.

    If a node representing code not included in the represented source is encountered, the iterator emits the artificial
    directive:
        <non-local call $node_id>
    to signal the fact, then regularly proceeds by following the return arc.

    :param cfg: a control-flow graph representing the program
    :param entry_pnt: the entry point from which iteration should start, either in label form or as a line number
    :return: an iterator that produces ASMLine objects
    :raise ValueError: when the specified entry point does not belong to any node of the CFG
    """

    # Find the node containing the entry point
    # Be aware that the entry point *MUST* refer to an instruction; nodes only contain those.
    for nid in [n for n in cfg.nodes.keys() if "external" not in cfg.nodes[n]]:
        view: FragmentView = cfg.nodes[nid]["block"]
        if view.begin <= entry_pnt < view.end:
            current_node = nid
            break
    else:
        raise ValueError("Invalid entry-point: no statement at line " + str(entry_pnt) + "is contained in this graph")

    # Prepare objects for iteration
    block: FragmentView = cfg.nodes[current_node]["block"]
    line_iterator: Iterator[ASMLine] = to_line_iterator(block.iter(entry_pnt), entry_pnt)
    line: ASMLine = next(line_iterator)

    execute_jump = yield line
    while True:
        # Advance 'till the end of the current block
        for line in line_iterator:
            execute_jump = yield line

        # Identify any conditional branch
        conditional = None
        for t, s in [(cfg.edges[current_node, s]["kind"], s) for s in cfg.successors(current_node)]:
            if t is Transition.C_JUMP:
                conditional = s
            else:
                # We don't expect more than one other "default" path to follow
                current_node = s

        # Set the conditional branch's destination as the current node, if the caller told us so
        if conditional is not None and execute_jump:
            current_node = conditional

        # If we're back at node 0, then execution has finished
        if current_node == 0:
            return

        # If the node we reached is external, just yield a special value and advance to the node that follows it
        if "external" in cfg.nodes[current_node]:
            yield ASMLine(-1, Directive("<non-local call " + str(current_node) + ">"))
            current_node = next(cfg.successors(current_node))

        # Load the next block and continue iteration
        block = cfg.nodes[current_node]["block"]
        line_iterator = to_line_iterator(iter(block), block.begin)


def merge_points(cfg: DiGraph) -> FrozenSet[int]:
    """
    Find all the merge point in the CFG.

    A merge point is a node on which multiple directed edges converge.

    :arg cfg: the CFG representing a program
    :return: a frozen set containing all the merge points
    """

    # Node 0 represents the calling environment, so it must be excluded from the analysis
    return frozenset((n for n in cfg.nodes.keys() if n != 0 and cfg.in_degree(n) > 1))


def loop_back_nodes(cfg: DiGraph) -> FrozenSet[int]:
    """
    Find all the nodes of a CFG that are exclusively part of a loop.

    A node is exclusively part of a loop if it belongs only to those paths that traverse the back-loop of a cycle.

    :arg cfg: the CFG representation of a program
    :return: a frozen set of all the loop-exclusive nodes
    """

    # Node 0 closes an improper loop over the CFG, so it must be ignored
    cycle_nodes = frozenset(chain.from_iterable(simple_cycles(restricted_view(cfg, [0], []))))
    return frozenset(cycle_nodes.difference(chain.from_iterable(
        # For every path, its last component is node 0; therefore, we have to cut it.
        map(lambda l: l[:-1], all_simple_paths(cfg, 1, 0)))))
