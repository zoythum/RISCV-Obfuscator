
from networkx import DiGraph, nx
from itertools import count
from rep.base import Instruction
from structures import opcodes


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


counter = count()


def populate_linelist(cfg: DiGraph, node_num: int) -> list:
    line_list = []
    line_number = cfg.nodes[node_num]["block"].begin
    for line in iter(cfg.nodes[node_num]["block"]):
        line_list.append((line_number, line))
        line_number += 1
    return line_list


def reg_read(regdict, reg, line, block_init):
    """
    manage the read of a register, if the register is already in the dict the endline of the last block associated to
    him is set to the current line,
    otherwise the register is added to the dictionary and a new block will be created
    :@param regdict: is the dictionary that store the register accessed in the node under analysis
    :@param reg: is the register accessed by the operation under analysis
    :@param line: is the line at which the operation occurs
    :@param block_init: the line at which start the block under analysis
    """

    if reg not in regdict.keys():
        block = ValueBlock(block_init, line, next(counter))
        regdict[reg] = [block]
    else:
        regdict[reg][-1].endline = line


def reg_write(block: ValueBlock, ln, localreg):
    line = ln[1]
    if line.r1 in localreg.keys():
        if localreg[line.r1][-1].endline == ln[0]:
            localreg[line.r1].append(block)
        else:
            localreg[line.r1][-1].endline = (ln[0] - 1)
            localreg[line.r1].append(block)
    else:
        localreg[line.r1] = [block]


def satisfy_contract_in(cfg: DiGraph, node, nodeid, regdict):
    """
    this function create an entry in the 'reg_bind' for every register that appear in the 'requires' contract of the
    node under analysis. The validity of the value assigned to these register is from the beginning to the end of the
    block of code contained in the node.
    :param node: the node under analysis
    :param regdict: the dictionary of the used registers
    """
    required = node['requires']
    for child in cfg.successors(nodeid):
        required = required.union(cfg.nodes[child]['requires'])
    for register in required:
        block = ValueBlock(node["block"].begin, node["block"].end - 1, next(counter))
        regdict[register] = [block]


def satisfy_contract_out(cfg: DiGraph, node, nodeid, regdict):
    """
    this function assure that the register in the 'requires' of the successors nodes have an assigned value, and then
    can't be modified, up to the end of the node's block of code.
    :param cfg: the graph of the analyzed program
    :param node: the node under analysis
    :param nodeid: the id of the node under analysis
    :param regdict: the dictionary of the used registers
    """
    required = set()
    for child in cfg.successors(nodeid):
        required = required.union(cfg.nodes[child]['requires'])
    for register in required:
        if regdict[register][-1].endline != node['block'].end:
            regdict[register][-1].endline = node['block'].end


def evaluate_instr(cfg: DiGraph, i: int, ln, localreg):
    line = ln[1]
    if opcodes[line.opcode][0] == 2:
        reg_read(localreg, line.r2, ln[0], cfg.nodes[i]['block'].begin)
    if opcodes[line.opcode][0] == 3:
        reg_read(localreg, line.r3, ln[0], cfg.nodes[i]['block'].begin)

    # Check if the opcode corresponds to a write operation
    if opcodes[line.opcode][1]:
        block = ValueBlock(ln[0], cfg.nodes[i]['block'].end - 1, next(counter))
        reg_write(block, ln, localreg)
    else:
        # the opcode correspond to a read operation
        reg_read(localreg, line.r1, ln[0], cfg.nodes[i]['block'].begin)


def bind_register_to_value(cfg: DiGraph, node: int = None):
    """
    This is the main function, it is responsible for the binding process that associate to every register used in a
    certain node a value. This association is represented by a dictionary that use as key the register's name and as
    value a list of block that contains the value holds by the register and it's range of validity
    :param node: [Optional] to run the algorithm only on a specific node
    :param cfg: the DiGraph that represent the program to be analyzed
    """
    if node is None:
        nodelist = list(nx.dfs_preorder_nodes(cfg, 0))
        # remove the exterior root node
        nodelist.remove(0)
    else:
        if node != 0:
            nodelist = [node]
            cfg.nodes[node].pop("reg_bind")
        else:
            return

    for i in nodelist:
        if ('reg_bind' in cfg.nodes[i]) or ('external' in cfg.nodes[i]):
            # this node is already analyzed so we skip it
            continue

        # linelist: contains tuple <'line_number', 'line'> of all the lines that compose the current node
        linelist = populate_linelist(cfg, i)
        # localreg: the dictionary that will be put into the node at the end of the binding process
        localreg = {}

        # bind the used registers to a symbolic value
        satisfy_contract_in(cfg, cfg.nodes[i], i, localreg)
        for ln in linelist:
            line = ln[1]
            if isinstance(line, Instruction) and (opcodes[line.opcode][0] != 0):
                evaluate_instr(cfg, i, ln, localreg)
        satisfy_contract_out(cfg, cfg.nodes[i], i, localreg)
        cfg.nodes[i]['reg_bind'] = localreg
