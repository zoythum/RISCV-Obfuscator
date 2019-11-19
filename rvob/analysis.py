from collections import deque
from enum import Enum, auto
from itertools import count
from typing import Sequence, Iterator, Mapping, Union, Tuple

from networkx import DiGraph

from rep.base import Instruction, Directive, ASMLine, to_line_iterator
from rep.fragments import CodeFragment, Source, FragmentView
from rvob.structures import jump_ops, JumpType


def get_stepper(fragments: Sequence[CodeFragment], entry_point: int = None) -> Iterator[ASMLine]:
    """
    Generate an instruction stepper over an ordered sequence of non-overlapping code fragments.

    The instruction stepper is an iterator over ASMLines that skips over any non-instruction statement, starting its
    iteration from the specified entry-point, or the first instruction of the first section otherwise.
    The fragments must be provided to this generator in an orderly fashion, devoid of overlaps, unless iteration order
    is not of concern. Keep in mind, though, that any instruction preceding the entry-point will be ignored.
    Contiguity between fragments is irrelevant.

    :param fragments: a sequence of ordered non-overlapping fragments
    :param entry_point: the line number from which the stepper should start iterating
    :return: an instruction stepper
    :raise IndexError: when the specified entry-point does not belong to the code contained in the fragments
    """

    # Start stepping from the first available line, if not told otherwise
    if entry_point is None:
        entry_point = fragments[0].get_begin()

    # Find the fragment from which we should start stepping
    for candidate in fragments:
        if candidate.get_begin() <= entry_point < candidate.get_end():
            starting_fragment_index = fragments.index(candidate)
            break
    else:
        # The entry-point falls out of range
        raise IndexError("The specified entry point doesn't belong to any of the provided sections")

    for fragment in fragments[starting_fragment_index:]:
        for line in to_line_iterator(iter(fragment), fragment.get_begin()):
            # Fast-forward until we find a line after the entry-point containing an instruction
            if line.number >= entry_point and type(line.statement) is Instruction:
                yield line


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

        # Instantiate the stepper for code exploration
        line_supplier = get_stepper(code_sections, start_line)
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

    # Create a list of fragments containing code
    code_sections = [tsec.scope for tsec in src.get_sections() if ".text" == tsec.identifier]

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


def flow_follower(cfg: DiGraph, sym_tab: Mapping[str, int], entry_pnt: Union[str, int] = "main"
                  ) -> Iterator[ASMLine]:
    # TODO add docstring
    if type(entry_pnt) is str:
        # Convert label to an actual entry point
        try:
            entry_pnt = sym_tab[entry_pnt]
        except KeyError:
            raise ValueError("Invalid entry-point: label \"" + entry_pnt + "\" does not exist")

    # Find the node containing the entry point
    # Be aware that the entry point *MUST* refer to an instruction; nodes only contain those.
    current_node = None
    for nid in cfg.nodes.keys():
        if "external" not in cfg.nodes[nid]:
            view: FragmentView = cfg.nodes[nid]["block"]
            if view.get_begin() <= entry_pnt < view.get_end():
                current_node = nid
                break

    if current_node is None:
        raise ValueError("Invalid entry-point: no statement at line " + entry_pnt + "is contained in this graph")

    # Prepare objects for iteration
    block: FragmentView = cfg.nodes[current_node]["block"]
    line_iterator: Iterator[ASMLine] = to_line_iterator(iter(block), block.get_begin())
    line: ASMLine = next(line_iterator)

    # Skip over lines preceding the entry point
    while line.number < entry_pnt:
        line = next(line_iterator)

    execute_jump = yield line
    while True:
        # Advance 'till the end of the current block
        for line in line_iterator:
            execute_jump = yield line

        # Singleton list containing the default follower
        default_follower = [node for node in cfg.successors(current_node)
                            if cfg.edges[current_node, node]["kind"] is not Transition.C_JUMP]
        # Singleton list containing the follower in case the caller decides to take a conditional branch, if any
        conditional_follower = [node for node in cfg.successors(current_node)
                                if cfg.edges[current_node, node]["kind"] is Transition.C_JUMP]

        # Choose the next node
        if len(conditional_follower) != 0 and execute_jump:
            current_node = conditional_follower[0]
        else:
            current_node = default_follower[0]

        # If we're back at node 0, then execution has finished
        if current_node == 0:
            return

        # If the node we reached is external, just yield a special value and advance to the node that follows it
        if "external" in cfg.nodes[current_node]:
            yield ASMLine(-1, Directive("<non-local call " + str(current_node) + ">"))
            current_node = next(cfg.successors(current_node))

        # Load the next block and continue iteration
        block = cfg.nodes[current_node]["block"]
        line_iterator = to_line_iterator(iter(block), block.get_begin())
