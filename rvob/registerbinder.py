from typing import List, Tuple, Dict

from networkx import DiGraph, nx
from itertools import count
from rep.base import Instruction, Statement
from structures import opcodes, Register


class ValueBlock:
    """
    These class represent a block that identifies a contiguous set of line, in a node, in which a certain register
    maintain the same value
    initline: the absolute number of the line from which the register have the value indicated in the block
    endline: the absolute number of the last line in which the register hold the value indicated by the block
    value: the value holds by the register
    scrambled: True if the the value pointed by the block was already scrambled, and so it's actual register isn't it's
                original one
    """

    def __init__(self, initline, endline, value: int, scrambled: bool = False):
        self.init_line = initline
        self.end_line = endline
        self.value = value
        self.scrambled = scrambled

    init_line: int
    end_line: int
    value: int
    scrambled: bool = False
    inserted: bool = False
    group_id: int = None
    not_modify: bool = False


counter = count()


def populate_linelist(cfg: DiGraph, node_num: int) -> List[Tuple[int, Statement]]:
    """
    Create a list of tuples which represent the line in a specific block of the graph.
    The tuple are of the form (line number, line)
    @param cfg: the graph of the program under analysis
    @param node_num: the id of the node under evaluations
    @return: the list of tuples representing the lines in the block
    """
    line_list = []
    line_number = cfg.nodes[node_num]["block"].begin
    for line in iter(cfg.nodes[node_num]["block"]):
        line_list.append((line_number, line))
        line_number += 1
    return line_list


def reg_read(regdict: Dict[Register, List[ValueBlock]], reg: Register, line: int, block_init: int):
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
        regdict[reg][-1].end_line = line


def reg_write(block: ValueBlock, ln: tuple, localreg: dict):
    """
    Manages an instruction that write something into its first register. If the register is already present into the
    localreg there are two possibilities, if the endline of the last ValueBlock correspond to the current line the new
    ValueBlock will be simply appended, otherwise the endline of the last ValueBlock will be setted to the current line
    and then the new ValueBlock will be appended
    @param block: a ValueBlock that starts from the current line till the end of the block in which the instruction appear
    @param ln: a tuple representing the line at which the instruction appears
    @param localreg: the reg_bind under constructions
    """
    line = ln[1]
    if line.r1 in localreg.keys():
        if localreg[line.r1][-1].end_line == ln[0]:
            localreg[line.r1].append(block)
        else:
            localreg[line.r1][-1].end_line = (ln[0] - 1)
            localreg[line.r1].append(block)
    else:
        localreg[line.r1] = [block]


def satisfy_contract_in(node: DiGraph.node, regdict: dict):
    """
    this function create an entry in the 'reg_bind' for every register that appear in the 'requires' contract of the
    node under analysis. The validity of the value assigned to these register is from the beginning to the end of the
    block of code contained in the node.
    :param node: the node under analysis
    :param regdict: the dictionary of the used registers
    """
    required = node['requires']
    for register in required:
        block = ValueBlock(node["block"].begin, node["block"].end - 1, next(counter))
        regdict[register] = [block]


def satisfy_contract_out(cfg: DiGraph, node: DiGraph.node, nodeid: int, regdict: dict):
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
        if (register in regdict) and (regdict[register][-1].end_line != (node['block'].end - 1)):
            block: ValueBlock = regdict[register][-1]
            block.end_line = node['block'].end - 1
            block.not_modify = True
        elif register not in regdict:
            block = ValueBlock(node["block"].begin, node["block"].end - 1, next(counter))
            block.not_modify = True
            regdict[register] = [block]


def is_scrambled(line: Instruction):
    """
    The function verify if the passed instruction changed it's first register from the original when, this is a signal
    that a scrambling is done
    @param line: the instruction to be inspected
    @return: true if the instruction's first register doesn't match with the instruction's original register
    """
    if line.original is None:
        return False
    else:
        if isinstance(line.original, Register):
            return not line.original.name == line.r1.name
        else:
            return not line.original.upper() == line.r1.name


def evaluate_instr(cfg: DiGraph, i: int, ln, localreg):
    """
    This function identify if the instruction is a only read instruction or if it's contains also write, based on this
    separation call the correct function to manage this instruction
    @param cfg: the graph of the program under analysis
    @param i: the number of the node under evaluation
    @param ln: a tuple representing a line of the program in the form (line number, line)
    @param localreg: the reg_bind under construction
    """
    line: Instruction = ln[1]
    if opcodes[line.opcode][0] == 2:
        reg_read(localreg, line.r2, ln[0], cfg.nodes[i]['block'].begin)
    if opcodes[line.opcode][0] == 3:
        reg_read(localreg, line.r3, ln[0], cfg.nodes[i]['block'].begin)

    # Check if the opcode corresponds to a write operation
    if opcodes[line.opcode][1]:
        block = ValueBlock(ln[0], cfg.nodes[i]['block'].end - 1, next(counter), is_scrambled(line))
        if line.inserted and not line.swap_instr:
            block.inserted = True
        reg_write(block, ln, localreg)
    else:
        # the opcode correspond to a read operation
        reg_read(localreg, line.r1, ln[0], cfg.nodes[i]['block'].begin)


def catch_the_previous_block(instruction: Instruction, line: int, reg_bind: Dict[Register, List[ValueBlock]]) \
        -> ValueBlock:
    """
    the function find the block, for a given register, that has a specific ending line
    @param instruction: the instruction from which extrapolate the register to be used as search-key
    @param line: the line number to be matched by the block
    @param reg_bind: the dictionary containing the ValueBlock
    @return: the block that match the register and the end_line
    """
    for block in reg_bind[instruction.r2]:
        if block.end_line == line:
            return block
    print()


def catch_the_actual_block(instruction: Instruction, line: int, reg_bind: Dict[Register, List[ValueBlock]]) \
        -> ValueBlock:
    """
    the function find the block, for a given register, that has a specific initial line
    @param instruction: the instruction from which extrapolate the register to be used as search-key
    @param line: the line number to be matched by the block
    @param reg_bind: the dictionary containing the ValueBlock
    @return: the block that match the register and the init_line
    """
    for block in reg_bind[instruction.r1]:
        if block.init_line == line:
            return block


def evaluate_fragmentation(line_list: List[Tuple[int, Statement]], reg_bind: Dict[Register, List[ValueBlock]]):
    """
    this function re-explore the lines of the node to see if there are some fragments, they can be individuated by the
    presence of a move instruction, with the swap_instr attribute set to True, that separate a ValueBlock into two
    fragment, if this instruction is find, then find the ValueBlock associated to the previous fragment, it's correspond
    to that ValueBlock that use the register read by the move instruction and that has as end_line the line of the move
    instruction, then find the block associated to the second fragment, has as register the register written by the move
    and as init_line the line of the move. At this point if the previous block doesn't have a group_id means this is the
    first fragmentation for the ValueBlock, assign to both the fragment the value associated to the previous ValueBlock,
    if the previous block has a group_id copy it to the actual block.
    @param line_list: the list of the couple line number, associated instruction
    @param reg_bind: the dictionary containing the ValueBlock sorted by register
    """
    for elm in line_list:
        if isinstance(elm[1], Instruction) and elm[1].swap_instr:
            actual_block: ValueBlock = catch_the_actual_block(elm[1], elm[0], reg_bind)
            prev_block: ValueBlock = catch_the_previous_block(elm[1], elm[0], reg_bind)
            if prev_block.group_id is None:
                prev_block.group_id = prev_block.value
            actual_block.group_id = prev_block.value
            actual_block.inserted = prev_block.inserted


def purge_external(cfg: DiGraph, nodelist: list):
    """
    Eliminates the external nodes, for them the reg_bind analysis isn't needed
    @param cfg: the graph of the program under analysis
    @param nodelist: the list of the nodes that compose the graph
    """
    nodelist[:] = (x for x in nodelist if 'external' not in cfg.nodes[x])


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
        purge_external(cfg, nodelist)
        # remove the exterior root node
    else:
        if node != 0 and 'external' not in cfg.nodes[node]:
            nodelist = [node]
            cfg.nodes[node].pop("reg_bind")
        else:
            return

    for i in nodelist:
        if 'reg_bind' in cfg.nodes[i]:
            cfg.nodes[i].pop("reg_bind")

        # linelist: contains tuple <'line_number', 'line'> of all the lines that compose the current node
        linelist = populate_linelist(cfg, i)
        # localreg: the dictionary that will be put into the node at the end of the binding process
        localreg = {}

        # bind the used registers to a symbolic value
        satisfy_contract_in(cfg.nodes[i], localreg)
        for ln in linelist:
            line = ln[1]
            if isinstance(line, Instruction) and (opcodes[line.opcode][0] != 0):
                evaluate_instr(cfg, i, ln, localreg)
        satisfy_contract_out(cfg, cfg.nodes[i], i, localreg)
        evaluate_fragmentation(linelist, localreg)
        cfg.nodes[i]['reg_bind'] = localreg
