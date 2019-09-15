from enum import Enum
from collections import deque
from bisect import bisect_right
import networkx as nx
import rvob.rep as rep

jump_type = Enum('JUMP', 'U, C')
# TODO what the hell do we do about 'jr' jumps?
jump_ops = {
    "call": jump_type.U,
    "j": jump_type.U,
    "jal": jump_type.U,
    "jalr": jump_type.U,
    "beq": jump_type.C,
    "bne": jump_type.C,
    "blt": jump_type.C,
    "bltu": jump_type.C,
    "bge": jump_type.C,
    "bgeu": jump_type.C
}


def build_cfg(src: rep.Source):
    label_dict = src.get_labels()
    # For now we only target '.text' sections
    sections = [sect for sect in src.get_sections() if sect[0].__eq__(".text")]
    # Fill a list containing the sections' starting lines
    pegs = [sect[1] for sect in sections]

    # Initialize the graph object and add an empty root node
    cfg = nx.DiGraph()
    cfg.add_node(-1, block=None)

    # Load the exploration stack with the first line of the first code section, setting the root node as initial father
    exs = deque()
    exs.append((sections[0][1], -1, frozenset()))

    # Set the flag to temporarily ignore labels to false
    ignore_labels = False

    # Perform a DFS for each element on the exploration stack
    while exs.__len__() != 0:
        dst, father, trail = exs.pop()
        # Extract section
        curr_sec = sections[bisect_right(pegs, dst) - 1]
        # Align local cursor
        cursor = dst - curr_sec[1]

        # If a loop is detected, add the looping edge to the graph and continue with the next iteration
        if dst in trail:
            cfg.add_edge(father, dst)
            continue

        # Add the new block to the trail
        trail = frozenset(list(trail) + [dst])

        # Advance until we encounter either a jump, a label or the end of the section
        while cursor < curr_sec[3].__len__():
            statement = curr_sec[3][cursor]

            if statement.labels.__len__() != 0 and ignore_labels is False:
                # Labeled statement encountered: set current line as block terminator and push the next line on exs
                stop = curr_sec[1] + cursor
                exs.append((stop, dst, trail))
                ignore_labels = True
                break
            elif type(statement) is rep.Instruction and jump_ops.keys().__contains__(statement.opcode):
                # Last line of the current block is a jump
                stop = curr_sec[1] + cursor + 1

                # If conditional jump, push the line that follows on the exploration stack
                if jump_type.C == jump_ops[statement.opcode]:
                    exs.append((stop, dst, trail))

                # Push the jump's target onto the exploration stack
                # TODO what the hell do we do about 'jr' jumps?
                try:
                    exs.append((label_dict[statement.instr_args["immediate"]], dst, trail))
                except KeyError:
                    # Jump to non-local code: execution resumes from the next line onwards
                    exs.append((stop, dst, trail))
                break
                
            cursor += 1
            ignore_labels = False
        else:
            # Hit end of section: set ending line as block end
            stop = curr_sec[2]

            # If this isn't the last section, push the next one's starting line on the exploration stack
            if curr_sec[2] != pegs[pegs.__len__() - 1]:
                exs.append((pegs[bisect_right(pegs, curr_sec[2]) - 1], dst, trail))

        # Add the new block to the CFG
        cfg.add_node(dst, block=src.lines[dst:stop])
        cfg.add_edge(father, dst)

    return cfg
