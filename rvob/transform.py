from collections import deque
from itertools import count
from typing import Sequence, Iterator

from networkx import DiGraph

from rep.base import Instruction, ASMLine, to_line_iterator
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


def build_cfg(src: Source, entry_point: str = "main") -> DiGraph:
    """
    Builds the CFG of the supplied assembly code, starting from the specified entry point.
    
    The entry point consists of a valid label pointing to what will be considered by the algorithm as the first
    instruction executed by a caller.
    The graph is built through a recursive DFS algorithm that follows the control flow.
    The resulting graph's nodes either contain a reference to a view, which represents the block of serial instructions
    associated with the node, or an `external` flag, signifying that the referenced code is external to the analyzed
    code.
    
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
                cfg.add_edge(rid, _explorer(line.number, __ret_stack__))
                break
            elif line.statement.opcode in jump_ops:
                # Create node
                cfg.add_node(rid, block=FragmentView(src, start_line, line.number + 1, start_line))
                ancestors[start_line] = rid

                if jump_ops[line.statement.opcode] == JumpType.U:
                    # Unconditional jump: resolve destination and relay-call explorer there
                    cfg.add_edge(rid,
                                 _explorer(label_dict[line.statement.instr_args["immediate"].symbol], __ret_stack__))
                    break
                elif jump_ops[line.statement.opcode] == JumpType.F:
                    # Function call: start by resolving destination
                    target = line.statement.instr_args["immediate"].symbol
                    # TODO find a way to modularize things so that this jump resolution can be moved out of its nest
                    try:
                        dst = label_dict[target]
                        # Update the return address
                        ret_stack.append(next(line_supplier).number)
                        # Set the current node as ancestor for the recursive explorer
                        home = rid
                    except KeyError:
                        # Calling an external function: add an edge to the external code node
                        if not cfg.has_node(target):
                            # First time we call this procedure, so we add its virtual node to the graph
                            # The keyword external means that this node contains code that is not in the source file
                            cfg.add_node(target, external=True)

                        cfg.add_edge(rid, target)

                        # Set the following line as destination
                        dst = next(line_supplier).number
                        # Set the external node as ancestor for the recursive explorer
                        home = target

                    # Perform the actual recursive call
                    cfg.add_edge(home, _explorer(dst, __ret_stack__))
                    break
                elif jump_ops[line.statement.opcode] == JumpType.C:
                    # Conditional jump: launch two explorers, one at the jump's target and one at the following line
                    cfg.add_edge(rid, _explorer(next(line_supplier).number, __ret_stack__))
                    # The second explorer needs a copy of the return stack, since it may encounter another return jump
                    cfg.add_edge(rid,
                                 _explorer(label_dict[line.statement.instr_args["immediate"].symbol],
                                           __ret_stack__.copy()))
                    break
                elif jump_ops[line.statement.opcode] == JumpType.R:
                    # Procedure return: close the edge on the return address by invoking an explorer there
                    cfg.add_edge(rid, _explorer(__ret_stack__.pop(), __ret_stack__))
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

    cfg.add_edge(root_id, child_id)

    return cfg
