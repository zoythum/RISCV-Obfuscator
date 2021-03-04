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

    def __str__(self):
        return "init_line:" + str(self.init_line) + "\n" + "end_line:" + str(
            self.end_line) + "\n" + "not_modify:" + str(self.not_modify) + "\n"


class SuperBlock:
    node_id: int
    register: Register
    value_block: ValueBlock

    def __init__(self, node: int, register: Register, block: ValueBlock):
        self.node_id = node
        self.register = register
        self.value_block = block


counter = count()
first_choice_blocks: List[SuperBlock] = []
second_choice_blocks: List[SuperBlock] = []
last_choice_blocks: List[SuperBlock] = []


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


def reg_read(reg_bind: Dict[Register, List[ValueBlock]], reg: Register, line: int, block_init: int):
    """
    manage the read of a register, if the register is already in the dict the endline of the last block associated to
    him is set to the current line,
    otherwise the register is added to the dictionary and a new block will be created
    :@param regdict: is the dictionary that store the register accessed in the node under analysis
    :@param reg: is the register accessed by the operation under analysis
    :@param line: is the line at which the operation occurs
    :@param block_init: the line at which start the block under analysis
    """

    if reg not in reg_bind.keys():
        block = ValueBlock(block_init, line, next(counter))
        reg_bind[reg] = [block]
    else:
        reg_bind[reg][-1].end_line = line


def reg_write(ln: tuple, reg_bind: dict):
    """
    Manages an instruction that write something into its first register.
    @param block: a ValueBlock that starts from the current line till the end of the block in which the instruction appears
    @param ln: a tuple representing the line at which the instruction appears
    @param reg_bind: the reg_bind under constructions
    """
    instruction = ln[1]
    block = ValueBlock(ln[0], ln[0], next(counter), is_scrambled(instruction))
    if instruction.inserted and not instruction.swap_instr:
        block.inserted = True

    if instruction.r1 in reg_bind.keys():
        reg_bind[instruction.r1].append(block)
    else:
        reg_bind[instruction.r1] = [block]


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
        block = ValueBlock(node["block"].begin, node["block"].begin, next(counter))
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
        try:
            block: ValueBlock = regdict[register][-1]
            block.end_line = node['block'].end - 1
            block.not_modify = True
        except KeyError:
            block = ValueBlock(node["block"].begin, node["block"].end - 1, next(counter))
            block.not_modify = True
            regdict[register] = [block]


def evaluate_instr(cfg: DiGraph, i: int, ln, reg_bind):
    """
    This function identify if the instruction is a only read instruction or if it's contains also write, based on this
    separation call the correct function to manage this instruction
    @param cfg: the graph of the program under analysis
    @param i: the number of the node under evaluation
    @param ln: a tuple representing a line of the program in the form (line number, instruction)
    @param reg_bind: the reg_bind under construction
    """
    instruction: Instruction = ln[1]
    # check if the instruction uses at least two registers, in this case the second argument of the instruction is a
    # register used in read mode, so update binding dictionary
    if opcodes[instruction.opcode][0] >= 2:
        reg_read(reg_bind, instruction.r2, ln[0], cfg.nodes[i]['block'].begin)
    # check if the instruction uses three registers, in this case the third argument of the instruction is a
    # register used in read mode, so update binding dictionary
    if opcodes[instruction.opcode][0] == 3:
        reg_read(reg_bind, instruction.r3, ln[0], cfg.nodes[i]['block'].begin)

    # Check if the opcode corresponds to a write operation
    if opcodes[instruction.opcode][1]:
        reg_write(ln, reg_bind)
    else:
        # the opcode correspond to a read operation
        reg_read(reg_bind, instruction.r1, ln[0], cfg.nodes[i]['block'].begin)


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
        if line == block.end_line:
            return block
        elif block.init_line == line:
            return None


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
            if prev_block is not None:
                if prev_block.group_id is None:
                    prev_block.group_id = prev_block.value
                actual_block.group_id = prev_block.value
                actual_block.inserted = prev_block.inserted
            else:
                actual_block.group_id = actual_block.value


def assign_blocks_to_list(node_id: int, reg_bind: Dict[Register, List[ValueBlock]]):
    global first_choice_blocks
    global second_choice_blocks
    global last_choice_blocks

    for reg in reg_bind.keys():
        for block in reg_bind[reg]:
            if not block.not_modify and (block.end_line - block.init_line) > 1:
                if not block.scrambled and block.group_id is None:
                    first_choice_blocks.append(SuperBlock(node_id, reg, block))
                elif not block.scrambled and block.group_id is not None:
                    second_choice_blocks.append(SuperBlock(node_id, reg, block))
                else:
                    last_choice_blocks.append(SuperBlock(node_id, reg, block))


def purge_external(cfg: DiGraph, nodelist: list):
    """
    Eliminates the external nodes, for them the reg_bind analysis isn't needed
    @param cfg: the graph of the program under analysis
    @param nodelist: the list of the nodes that compose the graph
    """
    nodelist[:] = (x for x in nodelist if 'external' not in cfg.nodes[x])


def debug_analysis(cfg: DiGraph):
    global first_choice_blocks
    global second_choice_blocks
    global last_choice_blocks

    block_num: int = 0
    for node_id in cfg.nodes:
        node = cfg.nodes[node_id]
        if 'external' not in node:
            reg_bind: Dict[Register, List[ValueBlock]] = node['reg_bind']
            for lists in reg_bind.values():
                block_num += len(lists)


def bind_register_to_value(cfg: DiGraph, node: int = None):
    """
    This is the main function, it is responsible for the binding process that associate to every register used in a
    certain node a value. This association is represented by a dictionary that use as key the register's name and as
    value a list of block that contains the value holds by the register and it's range of validity
    :param node: [Optional] to run the algorithm only on a specific node
    :param cfg: the DiGraph that represent the program to be analyzed
    """
    global first_choice_blocks
    global second_choice_blocks
    global last_choice_blocks

    first_choice_blocks.clear()
    second_choice_blocks.clear()
    last_choice_blocks.clear()

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
        assign_blocks_to_list(i, localreg)
        cfg.nodes[i]['reg_bind'] = localreg
    debug_analysis(cfg)
