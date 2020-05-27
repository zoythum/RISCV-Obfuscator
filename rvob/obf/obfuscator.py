from enum import Enum
from random import seed, randint, sample, choice
from typing import List, NamedTuple, Tuple, Mapping
from obf.const_derivation import generate_derivation_chain, Promise, primers
from rep.base import Instruction, to_line_iterator
from analysis.heatmaps import register_heatmap, mediate_heat
from structures import Register, opcd_family, not_modifiable_regs
from networkx import DiGraph
from queue import Queue


class NodeBlock:
    """
    A utility object that contains all the data that are relevant for the process of choosing where to put the
    instructions in a node
    @var node_id: the id of the node represented by the block
    @var init_line: the first line where you can insert an instruction
    @var end_line: the last line where you can insert an instruction
    """
    def __init__(self, node_id: int, init_line: int, end_line: int):
        self.node_id = node_id
        self.init_line = init_line
        self.end_line = end_line

    node_id: int
    init_line: int
    end_line: int


class Report(NamedTuple):
    """
    An object that contains all the information needed to complete the process of distributing a set of instructions
    between as many nodes as possible
    @var node_chain: a list of NodeBlock, one for each node in which is possible insert some instructions
    @var reg_pool: the set of all the free reg, obtained as the intersection of free reg for each node in the node_chain
    """
    node_chain: List[NodeBlock]
    reg_pool: set


def evaluate_next_node(cfg: DiGraph, actual_node: int, reg_pool: set, ndd_reg: int, register):
    successors = list(node for node in cfg.successors(actual_node))
    if (len(successors) >= 2) or ('external' in cfg.nodes[successors[0]]):
        return None
    else:
        actual_node = successors[0]
        predecessors = list(node for node in cfg.predecessors(actual_node))
        new_pool = reg_pool - set(reg.name for reg in cfg.nodes[actual_node]["reg_bind"].keys())
        if (len(new_pool) < ndd_reg) or (len(predecessors) >= 2):
            return None
        actual_block = cfg.nodes[actual_node]["block"]
        node_block = NodeBlock(actual_node, actual_block.begin, actual_block.begin)
        first = actual_block[node_block.init_line]
        if len(first.labels) != 0:
            if (first.r2 == register) or (first.r3 == register):
                return None
            else:
                node_block.init_line += 1
        tup = (node_block, new_pool)
        return tup


def calc_nodes_chain(cfg: DiGraph, start_node: int, start_line: int, register: Register, ndd_reg: int) -> Report:
    """
    This function search for all the valid node in which an instruction ca be added. The valid node are those that
    doesn't have sibling nodes. A node is valid until the line in which the rd register of the non-obfuscated
    instruction is used
    @param cfg: the graph that represents the assembly program
    @param start_node: the node where is present the instruction that will be obfuscated
    @param start_line: the line of the instruction that will be obfuscated
    @param register: the destination register used by the instruction that will be obfuscated
    @param ndd_reg: the number of register needed by the set of instructions that substitute the non-obfuscated one
    @return: a report object
    """
    actual_node = start_node
    actual_block = cfg.nodes[actual_node]["block"]
    reg_pool = set(Register.list())
    reg_pool -= not_modifiable_regs
    reg_pool -= set(reg for reg in cfg.nodes[start_node]["reg_bind"].keys())
    node_chain = [NodeBlock(start_node, start_line, start_line)]
    if start_line == (cfg.nodes[start_node]['block'].end - 1):
        node = evaluate_next_node(cfg, actual_node, reg_pool, ndd_reg, register)
        if node is None:
            return Report(node_chain, reg_pool)
        else:
            node_chain.append(node[0])
            reg_pool = node[1]
            actual_node = node[0].node_id
            actual_block = cfg.nodes[node[0].node_id]['block']
            line = node[0].init_line
    else:
        line = start_line
    while True:
        for instr in actual_block.iter(line):
            if (instr.r2 == register) or (instr.r3 == register):
                return Report(node_chain, reg_pool)
            node_chain[-1].end_line += 1
        node = evaluate_next_node(cfg, actual_node, reg_pool, ndd_reg, register)
        if node is None:
            return Report(node_chain, reg_pool)
        else:
            node_chain.append(node[0])
            reg_pool = node[1]
            line = node[0].init_line
            actual_node = node[0].node_id
            actual_block = cfg.nodes[node[0].node_id]['block']


def maximize_unused_reg_usage(cfg: DiGraph, report: Report, needed_reg: int):
    heat_map = register_heatmap(cfg, 50)
    mean_heat_node = list()
    try:
        for node in report.node_chain:
            actual_block = cfg.nodes[node.node_id]["block"]
            temp_list = [heat_map[x] for x in range(actual_block.begin, actual_block.end)]
            mean_heat_node.append(mediate_heat(temp_list))
        mean_heat = mediate_heat(mean_heat_node)
    except KeyError:
        mean_heat = [0]*len(Register.list())

    def sorting(val: Enum):
        return mean_heat[val.value]

    available_reg = list(report.reg_pool)
    available_reg.sort(key=sorting)
    valid_reg = set()
    for reg in available_reg:
        if mean_heat[reg.value] == 0 or len(valid_reg) < needed_reg:
            valid_reg.add(reg)
        else:
            break

    report._replace(reg_pool=valid_reg)


def calc_unresolved_register(prm_chain: List[Promise]) -> int:
    """
    This function calculates the number of unresolved registers
    @param prm_chain: a list of promises
    @return: the number of needed free registers
    """
    virtual_reg = set()
    for promise in prm_chain:
        if isinstance(promise.rd, int):
            virtual_reg.add(promise.rd)
        if isinstance(promise.rs1, int):
            virtual_reg.add(promise.rs1)
        if isinstance(promise.rs2, int):
            virtual_reg.add(promise.rs2)
    return len(virtual_reg)


def generate_positions(report: Report, obj_num: int) -> List[Tuple[int, List[int]]]:
    """
    the function select randomly the positions in which insert the instructions that is the obfuscated version of a
    previously chosen instruction
    @param report: a Report object generated by calc_nodes_chain
    @param obj_num: the number of the instructions that will substitute the non-obfuscated one
    @return: a list of tuples of the type: (node_id, list of lines in which insert the instructions)
    """
    seed()
    positions = list()
    # redistribute the promises over the selected nodes
    a = sample(range(0, obj_num), len(report.node_chain) - 1) + [0, obj_num]
    list.sort(a)
    b = [a[i+1] - a[i] for i in range(len(a) - 1)]
    for i in range(len(b)):
        node = report.node_chain[i].node_id
        pos = list()
        available_line = (report.node_chain[i].end_line - report.node_chain[i].init_line)
        if available_line >= b[i]:
            pos = sample(range(report.node_chain[i].init_line, report.node_chain[i].end_line), b[i])
            pos.sort()
        else:
            for x in range(b[i]):
                pos.append(report.node_chain[i].init_line + x)
        positions.append((node, pos))
    shift_amount = [0 for _ in range(len(positions))]
    for t in range(len(positions)):
        for t2 in range(0, t):
            if t != t2 and len(positions[t2][1]) > 0 and len(positions[t][1]) > 0 and positions[t2][1][0] < positions[t][1][0]:
                shift_amount[t] += len(positions[t2][1])
    for t in range(len(positions)):
        for t2 in range(len(positions[t][1])):
            positions[t][1][t2] += shift_amount[t]
    return positions


def check_reg(register, matrix, reg_pool: set) -> str:
    """
    check if a register, that is contained in a promise, is clearly defined or is associated to a number that act as
    a pseudo-name; in this last case the function try to check if that pseudo-name is already solved to a real register
    otherwise chose randomly a free reg to associate to it
    @param register: the register to inspect
    @param matrix: the dictionary that contains all the association between pseudo-name and register already solved
    @param reg_pool: the set of free reg from which extract a new one to associate to a pseudo-name register
    @return: the name of a real register
    """
    if isinstance(register, int):
        try:
            reg = matrix[register]
        except KeyError:
            reg = reg_pool.pop()
            matrix[register] = reg
        return reg
    else:
        return register


def fix_original_instruction(line: int, new_instr: List[Tuple[int, List[int]]]):
    for i in range(len(new_instr)):
        for t in range(len(new_instr[i][1])):
            if new_instr[i][1][t] <= line:
                line += 1
    return line


def placer(cfg: DiGraph, promises: List[Promise], report: Report, target_instr: int) -> int:
    """
    the role of this function is to convert the promises into real instructions and insert these one in the previously
    identified positions
    @param target_instr:
    @param cfg: the graph that represent the assembly program
    @param promises: the list of promises
    @param report: the report generated by calc_nodes_chain
    """
    register_matrix = {}
    positions = generate_positions(report, len(promises))
    target_instr = fix_original_instruction(target_instr, positions)
    instr_queue = Queue()
    promises.reverse()
    for prom in promises:
        rd = check_reg(prom.rd, register_matrix, report.reg_pool)
        rs1 = check_reg(prom.rs1, register_matrix, report.reg_pool)
        rs2 = check_reg(prom.rs2, register_matrix, report.reg_pool)
        instr = Instruction(prom.op.name.lower(), opcd_family[prom.op.name.lower()], r1=rd, r2=rs1, r3=rs2, immediate=prom.const)
        instr_queue.put(instr)
    for i in range(len(positions)):
        active_block = cfg.nodes[positions[i][0]]['block']
        for t in range(len(positions[i][1])):
            line = positions[i][1][t]
            instr = instr_queue.get()
            active_block.insert(line, instr)
    return target_instr


def get_immediate_instructions(cfg) -> Tuple[int, int]:
    """
    The functions search for all the immediate instructions in the specified cfg and
    returns a tuple where the first parameter represents a node and the second one is a line number.
    :param cfg:
    :return: (node, line_num)
    """
    result = []
    for node in cfg.nodes:
        if "external" not in cfg.nodes[node]:
            current_node = cfg.nodes[node]
            iterator = to_line_iterator(current_node['block'].iter(current_node['block'].begin),
                                        current_node['block'].begin)
            while True:
                try:
                    line = iterator.__next__()
                    line_num = line.number
                    stat = line.statement
                    if (stat.opcode in primers or stat.opcode == "li") and stat.immediate is not None \
                            and stat.immediate.symbol is None:
                        result.append((node, line_num))
                except StopIteration:
                    break
    return choice(result)


def obfuscate(cfg: DiGraph, node_id: int = None, target_instr: int = None):
    """
    this is the main function that, given an instruction, generate the list of promises, convert them into instructions
    and distribute them in as many nodes as possible
    @param cfg: the graph that represent the assembly program
    @param node_id: the id of the node where is collocated the instruction to obfuscate
    @param target_instr: the line of the instruction to obfuscate
    """
    if node_id is None or target_instr is None:
        extracted = get_immediate_instructions(cfg)
        node_id = extracted[0]
        target_instr = extracted[1]
    instruction = cfg.nodes[node_id]["block"][target_instr]
    max_shift = randint(1, 10)
    max_logical = randint(1, 10)
    promise_chain = generate_derivation_chain(instruction, max_shift, max_logical)
    needed_reg = calc_unresolved_register(promise_chain)
    report = calc_nodes_chain(cfg, node_id, target_instr, instruction.r1, needed_reg)
    maximize_unused_reg_usage(cfg, report, needed_reg)
    target_instr = placer(cfg, promise_chain, report, target_instr)
    if len(instruction.labels) > 0:
        succ_instr = cfg.nodes[node_id]['block'][target_instr + 1]
        succ_instr.labels = instruction.labels
    del cfg.nodes[node_id]['block'][target_instr]
