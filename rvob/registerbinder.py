from enum import Enum
from itertools import count

from networkx import DiGraph, nx

from rvob import rep
from rvob.transform import SectionUnroller


class ValueBlock:
    def __init__(self, initline, endline, value: int):
        self.initline = initline
        self.value = value
        self.endline = endline


register_status = {}

value_count = count()

# Dictionary to classify the operations that perform a write on the first register,
# the keys in the dictionary indicates the amount of register used by the operations in the associated list
write_operations = {
    'single': ['lui', 'auipc', 'jal'],
    'double': ['jalr', 'lb', 'lh', 'lw', 'lbu', 'lhu', 'addi', 'slti', 'sltiu', 'xori', 'ori', 'andi', 'slli', 'srli',
               'srai', 'lwu', 'ld', 'addiw', 'slliw', 'srliw', 'sraiw', 'lr.w', 'lr.d'],
    'triple': ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and', 'addw', 'subw', 'sllw', 'srlw',
               'sraw', 'mul', 'mulh', 'mulhsu', 'div', 'divu', 'rem', 'remu', 'mulw', 'divw', 'divuw',
               'remw', 'remuw', 'sc.w', 'amoswap.w', 'amoadd.w', 'amoxor.w', 'amoor.w', 'amoand.w', 'amomin.w',
               'amomax.w', 'amominu.w', 'amomaxu.w', 'sc.d', 'amoswap.d', 'amoadd.d', 'amoxor.d', 'amoor.d',
               'amoand.d', 'amomin.d', 'amomax.d', 'amominu.d', 'amomaxu.d']
}

# Dictionary to classify the operations that read only from the register,
# the keys in the dictionary indicates the amount of register used by the operations in the associated list
read_operations = {
    'single': [],
    'double': ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'sb', 'sh', 'sw', 'sd'],
    'triple': []
}


def bind_register_to_value(cfg: DiGraph):
    nodelist = list(nx.dfs_preorder_nodes(cfg, 0))
    reader = SectionUnroller([tsec for tsec in src.get_sections() if ".text" == tsec.name])

    for i in nodelist:
        lineiterator = reader.get_line_iterator(reader, cfg.nodes[i]['start'])
        localreg = {}

        if 'reg_bind' in cfg.nodes[i]:
            # a loop is detected
            loop_manager(cfg, ,)
        for line in lineiterator:
            if type(line.st) is rep.Instruction:
                if line.st.opcode in write_operations['single']:
                    register_status[line.st.instr_args['r1']] = value_count.__next__()
                    block = ValueBlock(line, cfg.nodes[i]['end'], value_count)
                    if line.st.instr_args['r1'] in localreg.keys():
                        localreg[line.st.instr_args['r1']][-1].endline = (line - 1)
                        localreg[line.st.instr_args['r1']].append(block)
                    else:
                        localreg[line.st.instr_args['r1']] = [block]
                if line.st.opcode in write_operations['double']:
                    reg_read(localreg, line.st.instr_args['r2'], line)
                if line.st.opcode in write_operations['triple']:
                    reg_read(localreg, line.st.instr_args['r3'], line)
                if line.st.opcode in read_operations['single']:
                    reg_read(localreg, line.st.instr_args['r1'], line)
                if line.st.opcode in read_operations['double']:
                    reg_read(localreg, line.st.instr_args['r2'], line)
        cfg.nodes[i]['reg_bind'] = localreg


# manage a read operation performed on register 'reg' at the line number 'line', 'regdict' is the dictionary that store the register accessed in the node under analysis
# if the register is already in the dict the endline of the last block associated to him is set to the current line,
# otherwise the register is added to the dictionary and a new block will be created
def reg_read(regdict, reg, line):
    if reg not in regdict.keys():
        value_count.__next__()
        block = ValueBlock(line, line, value_count)
        regdict[reg] = [block]
    else:
        regdict[reg][-1].endline = line


def loop_manager(cfg: DiGraph, confreg: set, confnode: int, analizednode:int):
    newconfreg = []
    for val in confreg:
        (ValueBlock)(cfg.nodes[analizednode]['reg_bind'][val][-1]).value = (ValueBlock)(cfg.nodes[confnode]['reg_bind'][val][-1]).value
        if len(cfg.nodes[analizednode]['reg_bind'][val]) == 1:
            newconfreg.append(val)
    pred = list(cfg.predecessors(analizednode))
    if (len(newconfreg) > 0) and (len(pred) == 1):
        loop_manager(cfg, set(newconfreg), confnode, pred[1])