import copy
import itertools

from networkx import DiGraph, nx
from rvob.structures import opcodes
from rvob.rep.base import Instruction


class ValueBlock:
    """
    These class represent a block that identifies a contiguous set of line, in a node, in which a certain register
    maintain the same value
    initline: the absolute number of the line from which the register have the value indicated in the block
    endline: the absolute number of the last line in which the register hold the value indicated by the block
    value: the value holds by the register
    """

    def __init__(self, initline, endline, value: int):
        self.initline = initline
        self.endline = endline
        self.value = value


counter = itertools.count()


def reg_read(regdict, reg, line):
    """
    manage the read of a register, if the register is already in the dict the endline of the last block associated to
    him is set to the current line,
    otherwise the register is added to the dictionary and a new block will be created
    :param regdict: is the dictionary that store the register accessed in the node under analysis
    :param reg: is the register accessed by the operation under analysis
    :param line: is the line at which the operation occurs
    """

    if reg not in regdict.keys():
        block = ValueBlock(line, line, counter.__next__())
        regdict[reg] = [block]
    else:
        regdict[reg][-1].endline = line


def bind_register_to_value(cfg: DiGraph):
    """
    This is the main function, it is responsible for the binding process that associate to every register used in a
    certain node a value. This association is represented by a dictionary that use as key the register's name and as
    value a list of block that contains the value holds by the register and it's range of validity
    :param cfg: the DiGraph that represent the program to be analyzed
    """

    nodelist = list(nx.dfs_preorder_nodes(cfg, 0))
    # remove the exterior root node
    nodelist.remove(0)

    for i in nodelist:
        # linelist: contains tuple <'line_number', 'line'> of all the lines that appartains to the current node
        linelist = []
        # localreg: the dictionary that will be put into the node at the end of the binding process
        localreg = {}

        line_number = cfg.nodes[i]["block"].get_begin()
        for line in cfg.nodes[i]["block"]:
            linelist.append((line_number, line))
            line_number += 1

        if 'reg_bind' not in cfg.nodes[i]:
            for l in linelist:
                line = l[1]
                if type(line) is Instruction:
                    if opcodes[line.opcode][0] == 2:
                        reg_read(localreg, line.r2, l[0])
                    if opcodes[line.opcode][0] == 3:
                        reg_read(localreg, line.r3, l[0])

                    # Check if the opcode corresponds to a write operation
                    if opcodes[line.opcode][1]:
                        block = ValueBlock(l[0], cfg.nodes[i]['block'].get_end(), counter.__next__())
                        if line.r1 in localreg.keys():
                            if localreg[line.r1][-1].endline == l[0]:
                                localreg[line.r1].append(block)
                            else:
                                localreg[line.r1][-1].endline = (l[0] - 1)
                                localreg[line.r1].append(block)
                        else:
                            localreg[line.r1] = [block]
                    else:
                        # the opcode correspond to a read operation
                        reg_read(localreg, line.r1, l[0])
            cfg.nodes[i]['reg_bind'] = localreg
