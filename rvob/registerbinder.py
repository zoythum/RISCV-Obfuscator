import copy

from networkx import DiGraph, nx
from rvob.structures import opcodes

import rvob.rep as rep


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


class Counter:
    def __init__(self):
        self.value = 0

    def __next__(self):
        self.value += 1

    def getvalue(self):
        return self.value


# a global register to maintain the last value kept by a register
register_status = {}
snapshot_register_copy = {}
value_count = Counter()


def reg_read(regdict, reg, line, actval):
    """
    manage the read of a register, if the register is already in the dict the endline of the last block associated to him is set to the current line,
    otherwise the register is added to the dictionary and a new block will be created
    :param regdict: is the dictionary that store the register accessed in the node under analysis
    :param reg: is the register accessed by the operation under analysis
    :param line: is the line at which the operation occurs
    :param actval: the last value assigned to the register if exist, otherwise None
    """

    if reg not in regdict.keys():
        if actval is None:
            value_count.__next__()
            block = ValueBlock(line, line, value_count.getvalue())
            register_status[reg] = value_count.getvalue()
        else:
            block = ValueBlock(line, line, actval)
        regdict[reg] = [block]
    else:
        regdict[reg][-1].endline = line


def loop_manager(cfg: DiGraph, confreg: set, confnode: int, analizednode: int):
    """

    :param cfg: the DiGraph representing the program under analysis
    :param confreg: the set containing the register that are conflicting
    :param confnode: the node that already have a reg-value binding dictionary
    :param analizednode: the predecessor node of the conflicting ones
    """
    newconfreg = []
    for val in confreg:
        cfg.nodes[analizednode]['reg_bind'][val][-1].value = cfg.nodes[confnode]['reg_bind'][val][-1].value
        if len(cfg.nodes[analizednode]['reg_bind'][val]) == 1:
            newconfreg.append(val)
    pred = list(cfg.predecessors(analizednode))
    if (len(newconfreg) > 0) and (len(pred) == 1) and (pred[0] != confnode):
        loop_manager(cfg, set(newconfreg), confnode, pred[0])


def bind_register_to_value(cfg: DiGraph):
    """
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

        if i in snapshot_register_copy:
            global register_status
            register_status = snapshot_register_copy[i]

        if 'reg_bind' not in cfg.nodes[i]:
            for l in linelist:
                line = l[1]
                if type(line) is rep.Instruction:
                    if opcodes[line.opcode][0] == 2:
                        if line.instr_args['r2'] in register_status:
                            reg_read(localreg, line.instr_args['r2'], l[0], register_status[line.instr_args['r2']])
                        else:
                            reg_read(localreg, line.instr_args['r2'], l[0], None)
                    if opcodes[line.opcode][0] == 3:
                        if line.instr_args['r3'] in register_status:
                            reg_read(localreg, line.instr_args['r3'], l[0], register_status[line.instr_args['r3']])
                        else:
                            reg_read(localreg, line.instr_args['r3'], l[0], None)
                    # Check if the opcode corresponds to a write operation
                    if opcodes[line.opcode][1]:
                        value_count.__next__()
                        block = ValueBlock(l[0], cfg.nodes[i]['block'].get_end(), value_count.getvalue())
                        if line.instr_args['r1'] in localreg.keys():
                            localreg[line.instr_args['r1']][-1].endline = (l[0] - 1)
                            localreg[line.instr_args['r1']].append(block)
                        else:
                            localreg[line.instr_args['r1']] = [block]
                            register_status[line.instr_args['r1']] = value_count.getvalue()
                    else:
                        # the opcode correspond to a read operation
                        if line.instr_args['r1'] in register_status:
                            reg_read(localreg, line.instr_args['r1'], l[0], register_status[line.instr_args['r1']])
                        else:
                            reg_read(localreg, line.instr_args['r1'], l[0], None)
            cfg.nodes[i]['reg_bind'] = localreg
            childnodes = list(cfg.successors(i))
            if len(childnodes) >= 2:
                for n in range(len(childnodes)):
                    if childnodes[n] != nodelist[i]:
                        snapshot_register_copy[childnodes[n]] = copy.deepcopy(register_status)
