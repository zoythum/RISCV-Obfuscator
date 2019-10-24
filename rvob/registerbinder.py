from networkx import DiGraph, nx

import rvob.rep as rep
import json
import rvob.transform as transform


class ValueBlock:
    def __init__(self, initline, endline, value: int):
        self.initline = initline
        self.value = value
        self.endline = endline


class Counter:
    def __init__(self):
        self.value = 0

    def __next__(self):
        self.value += 1

    def getvalue(self):
        return self.value


register_status = {}
value_count = Counter()

opcodes = {
    'lui': (1, True), 'auipc': (1, True), 'jal': (1, True), 'jalr': (2, True), 'lb': (2, True), 'lh': (2, True),
    'lw': (2, True), 'lbu': (2, True), 'lhu': (2, True), 'addi': (2, True), 'slti': (2, True),
    'sltiu': (2, True), 'xori': (2, True), 'ori': (2, True), 'andi': (2, True), 'slli': (2, True),
    'srli': (2, True), 'srai': (2, True), 'lwu': (2, True), 'ld': (2, True), 'addiw': (2, True),
    'slliw': (2, True), 'srliw': (2, True), 'sext.w': (2, True), 'mv': (2, True), 'sraiw': (2, True), 'lr.w': (2, True),
    'lr.d': (2, True), 'add': (3, True), 'sub': (3, True), 'sll': (3, True), 'slt': (3, True),
    'sltu': (3, True), 'xor': (3, True), 'srl': (3, True), 'sra': (3, True), 'or': (3, True), 'and': (3, True),
    'addw': (3, True), 'subw': (3, True), 'sllw': (3, True), 'srlw': (3, True), 'sraw': (3, True), 'mul': (3, True),
    'mulh': (3, True), 'mulhsu': (3, True), 'div': (3, True), 'divu': (3, True), 'rem': (3, True),
    'remu': (3, True), 'mulw': (3, True), 'divw': (3, True), 'divuw': (3, True), 'remw': (3, True),
    'remuw': (3, True), 'sc.w': (3, True), 'amoswap.w': (3, True), 'amoadd.w': (3, True),
    'amoxor.w': (3, True), 'amoor.w': (3, True), 'amoand.w': (3, True), 'amomin.w': (3, True), 'amomax.w': (3, True),
    'amominu.w': (3, True), 'amomaxu.w': (3, True), 'sc.d': (3, True), 'amoswap.d': (3, True), 'amoadd.d': (3, True),
    'amoxor.d': (3, True), 'amoor.d': (3, True), 'amoand.d': (3, True), 'amomin.d': (3, True),
    'amomax.d': (3, True), 'amominu.d': (3, True), 'amomaxu.d': (3, True), 'jr': (1, False), 'j': (1, False),
    'beq': (2, False), 'bne': (2, False), 'blt': (2, False), 'bge': (2, False), 'ble': (2, False), 'bltu': (2, False),
    'bgeu': (2, False), 'sb': (2, False), 'sh': (2, False), 'sw': (2, False), 'sd': (2, False), 'li': (1, True),
    'beqz': (1, False), 'bnez': (1, False), 'bgtu': (2, False), 'bleu': (2, False), 'nop': (0, False)
}


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


def bind_register_to_value(src: rep.Source, cfg: DiGraph):
    nodelist = list(nx.dfs_preorder_nodes(cfg, 0))
    nodelist.remove(0)
    reader = transform.SectionUnroller([tsec for tsec in src.get_sections() if ".text" == tsec.name])

    for i in nodelist:
        linelist = []
        localreg = {}

        for x in range(cfg.nodes[i]["start"], cfg.nodes[i]["end"], 1):
            linelist.append((x, src.lines[x]))

        if ('reg_bind' in cfg.nodes[i]) and ('reg_bind') in cfg.nodes[i-1]:
            # a loop is detected
            conflict = cfg.nodes[i]['reg_bind'] & cfg.nodes[i-1]['reg_bind']
            loop_manager(cfg, conflict, i, i-1)
        for l in linelist:
            line = l[1]
            if type(line) is rep.Instruction:
                # Check if the opcode corresponds to a write operation
                if opcodes[line.opcode][1]:
                    value_count.__next__()
                    block = ValueBlock(l[0], cfg.nodes[i]['end'], value_count.getvalue())
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
                if opcodes[line.opcode][0] == 2:
                    if line.instr_args['r2'] in register_status:
                        reg_read(localreg, line.instr_args['r2'], l[0], register_status[line.instr_args['r1']])
                    else:
                        reg_read(localreg, line.instr_args['r2'], l[0], None)
                if opcodes[line.opcode][0] == 3:
                    if line.instr_args['r3'] in register_status:
                        reg_read(localreg, line.instr_args['r3'], l[0], register_status[line.instr_args['r1']])
                    else:
                        reg_read(localreg, line.instr_args['r3'], l[0], None)
        cfg.nodes[i]['reg_bind'] = localreg
