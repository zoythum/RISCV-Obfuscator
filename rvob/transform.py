from enum import Enum
from collections import deque, namedtuple
from itertools import count
from bisect import bisect_right
from networkx import DiGraph
from rvob.rep import Instruction, Source

# Type of jumps:
# U: unconditional jump without side effects
# C: conditional jump/branching instruction
# F: unconditional jump with return-address memorization (procedure call)
# R: unconditional jump to memorized return-address (procedure return)
jump_type = Enum('JUMP', 'U, C, F, R')

# Dictionary of jump instructions
jump_ops = {
    "call": jump_type.F,
    "jr": jump_type.R,
    "j": jump_type.U,
    "jal": jump_type.F,
    "jalr": jump_type.F,
    "beq": jump_type.C,
    "beqz": jump_type.C,
    "bne": jump_type.C,
    "bnez": jump_type.C,
    "blt": jump_type.C,
    "bltz": jump_type.C,
    "bltu": jump_type.C,
    "ble": jump_type.C,
    "blez": jump_type.C,
    "bleu": jump_type.C,
    "bgt": jump_type.C,
    "bgtz": jump_type.C,
    "bgtu": jump_type.C,
    "bge": jump_type.C,
    "bgez": jump_type.C,
    "bgeu": jump_type.C
}


# TODO Is this a good object? Can it belong to a narrower namespace?
class SectionUnroller:

    def __init__(self, sections):
        self.__header_lines__ = []
        self.__sections__ = {}

        for section in sections:
            self.__header_lines__.append(section.scope.get_begin())
            self.__sections__[section.scope.get_begin()] = section

    def get_containing_section(self, line_number: int):
        # Find a section that sports the last starting line that precedes the one passed as argument
        candidate = self.__sections__[self.__header_lines__[bisect_right(self.__header_lines__, line_number) - 1]]

        # Check for line membership: if the received line belongs to the candidate, return it, otherwise it is outside
        # of the sections selected for scanning
        if candidate.scope.get_begin() <= line_number < candidate.scope.get_end():
            return candidate
        else:
            raise KeyError

    def get_nearest_following_section(self, line_number: int):
        # Find the index of the __header_lines__ entry which could indicate the starting line of the nearest following
        # section
        tentative_index = bisect_right(self.__header_lines__, line_number)

        # Check if we've reached the end of the index and didn't find a suitable section
        if tentative_index == len(self.__header_lines__):
            raise ValueError
        else:
            # Return the nearest following section
            return self.__sections__[self.__header_lines__[tentative_index]]

    def get_following_line(self, line_number):
        # Get the section containing the received line
        current_section = self.get_containing_section(line_number)

        # Check code contiguity between the received line and the one which should follow
        if line_number < current_section.scope.get_end():
            return line_number + 1
        else:
            # If the following line falls outside of the section in which the received line resides, then such line must
            # be the header line of the following section
            return self.get_nearest_following_section(line_number + 1).scope.get_begin()

    def get_line_iterator(self, starting_line: int):
        line = namedtuple("Line", 'ln st')

        curr_line = starting_line
        while True:
            try:
                # If the starting line exists inside the considered sections, then find the section it belongs to
                curr_section = self.get_containing_section(curr_line)
            except KeyError:
                # The starting line falls outside of the considered sections, so the real starting line must be the
                # header line of the nearest following section wrt the stated starting line
                try:
                    curr_section = self.get_nearest_following_section(curr_line)
                    curr_line = curr_section.scope.get_begin()
                except ValueError:
                    # No nearest following section exists, so we must have reached the end
                    break

            for statement in curr_section.scope[curr_line:curr_section.scope.get_end()]:
                yield line(curr_line, statement)
                curr_line += 1


# TODO include some sort of code view inside nodes
def build_cfg(src: Source, entry_point: str = "main"):
    
    def explorer(start_line: int, __ret_stack__: deque):
        # Detect if there's a loop and eventually return the ancestor's ID to the caller
        if start_line in ancestors:
            return ancestors[start_line]

        line_supplier = reader.get_line_iterator(start_line)
        # Generate node ID for the root of the local subtree
        rid = id_sup.__next__()

        # Variable for keeping track of the previous line, in case we need to reference it
        previous_line = None

        for line in line_supplier:
            if len(line.st.labels) != 0 and line.ln != start_line:
                # TODO maybe we can make this iterative?
                # We stepped inside a new contiguous block: build the node for the previous block and relay
                cfg.add_node(rid, start=start_line, end=previous_line)
                ancestors[start_line] = rid
                cfg.add_edge(rid, explorer(line.ln, __ret_stack__))
                break
            elif type(line.st) is Instruction and line.st.opcode in jump_ops:
                # Create node
                cfg.add_node(rid, start=start_line, end=line.ln)
                ancestors[start_line] = rid

                if jump_ops[line.st.opcode] == jump_type.U:
                    # Unconditional jump: resolve destination and relay-call explorer there
                    cfg.add_edge(rid, explorer(label_dict[line.st.instr_args["immediate"]], __ret_stack__))
                    break
                elif jump_ops[line.st.opcode] == jump_type.F:
                    # Function call: start by resolving destination
                    target = line.st.instr_args["immediate"]
                    # TODO find a way to modularize things so that this jump resolution can be moved out of its nest
                    try:
                        dst = label_dict[target]
                        # Update the return address
                        ret_stack.append(reader.get_following_line(line.ln))
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
                        dst = reader.get_following_line(line.ln)
                        # Set the external node as ancestor for the recursive explorer
                        home = target

                    # Perform the actual recursive call
                    cfg.add_edge(home, explorer(dst, __ret_stack__))
                    break
                elif jump_ops[line.st.opcode] == jump_type.C:
                    # Conditional jump: launch two explorers, one at the jump's target and one at the following line
                    cfg.add_edge(rid, explorer(reader.get_following_line(line.ln), __ret_stack__))
                    # The second explorer needs a copy of the return stack, since it may encounter another return jump
                    cfg.add_edge(rid, explorer(label_dict[line.st.instr_args["immediate"]], __ret_stack__.copy()))
                    break
                elif jump_ops[line.st.opcode] == jump_type.R:
                    # Procedure return: close the edge on the return address by invoking an explorer there
                    cfg.add_edge(rid, explorer(__ret_stack__.pop(), __ret_stack__))
                    break
                else:
                    raise LookupError("Unrecognized jump type")

            previous_line = line.ln
        else:
            cfg.add_node(rid, start=start_line, end=previous_line)

        return rid

    # Generate the dictionary containing label mappings
    label_dict = src.get_labels()

    # Instantiate the section un-roller
    reader = SectionUnroller([tsec for tsec in src.get_sections() if ".text" == tsec.identifier])

    # Instantiate the node id supplier
    id_sup = count()

    # Instantiate an empty di-graph for hosting the CFG
    cfg = DiGraph()
    
    # Initialize the dictionary mapping blocks' initial lines to nodes
    ancestors = {}

    # Initialize the graph with a special root node
    root_id = id_sup.__next__()
    cfg.add_node(root_id, external=True)
    ancestors[-1] = root_id

    # Initialize the return stack
    ret_stack = deque()
    ret_stack.append(-1)

    # Call the explorer on the entry point and append the resulting graph to the root node
    child_id = explorer(label_dict[entry_point], ret_stack)
    cfg.add_edge(root_id, child_id)

    return cfg
