from random import seed, randint, sample
from typing import List, NamedTuple, Tuple
from obf.const_derivation import generate_derivation_chain, Promise
from rep.base import Instruction
from structures import Register, opcd_family
from networkx import DiGraph


class NodeBlock:

    def __init__(self, node_id: int, init_line: int, end_line: int):
        self.node_id = node_id
        self.init_line = init_line
        self.end_line = end_line

    node_id: int
    init_line: int
    end_line: int


class Report(NamedTuple):
    node_chain: List[NodeBlock]
    reg_pool: set


def calc_nodes_chain(cfg: DiGraph, start_node: int, start_line: int, register: Register, ndd_reg: int) -> Report:
    actual_node = start_node
    actual_block = cfg.nodes[actual_node]["block"]
    reg_pool = set(reg.name for reg in Register)
    reg_pool -= set(reg.name for reg in cfg.nodes[start_node]["reg_bind"].keys())
    node_chain = [NodeBlock(start_node, start_line, start_line)]
    line = start_line
    while True:
        for instr in actual_block.iter(line):
            if (instr.r2 == register) or (instr.r3 == register):
                return Report(node_chain, reg_pool)
            node_chain[-1].end_line += 1
        successors = list(node for node in cfg.successors(actual_node))
        if len(successors) >= 2:
            return Report(node_chain, reg_pool)
        else:
            actual_node = successors[0]
            new_pool = reg_pool - set(reg.name for reg in cfg.nodes[actual_node]["reg_bind"].keys())
            if len(new_pool) < ndd_reg:
                return Report(node_chain, reg_pool)
            line = cfg.nodes[actual_node]["block"].begin
            actual_block = cfg.nodes[actual_node]["block"]
            node_chain.append(NodeBlock(actual_node, actual_block.begin, actual_block.begin))
            first = actual_block.pop(line)
            if len(first.labels) != 0:
                if (first.r2 == register) or (first.r3 == register):
                    del node_chain[-1]
                    return Report(node_chain, reg_pool)
                else:
                    node_chain[-1].init_line += 1
            actual_block.insert(line, first)
            reg_pool = new_pool


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
    seed()
    positions = list()
    a = sample(range(0, obj_num), len(report.node_chain) - 1) + [0, obj_num]
    list.sort(a)
    b = [a[i+1] - a[i] for i in range(len(a) - 1)]
    for i in range(len(b)):
        node = report.node_chain[i].node_id
        pos = list()
        try:
            pos = sample(range(report.node_chain[i].init_line, report.node_chain[i].end_line), b[i])
            pos.sort()
        except ValueError:
            for _ in range(b[i]):
                pos.append(report.node_chain[i].init_line)
        for t in range(len(pos)):
            if (i != 0) and (pos[0] > positions[-1][1][0]):
                pos[t] += t + len(positions[-1][1])
            else:
                pos[t] += t
        positions.append((node, pos))
    return positions


def check_reg(register, matrix, reg_pool: set) -> str:
    if isinstance(register, int):
        try:
            reg = matrix[register]
        except KeyError:
            reg = reg_pool.pop()
            matrix[register] = reg
        return reg
    else:
        return register


def placer(cfg: DiGraph, promises: List[Promise], report: Report):
    register_matrix = {}
    positions = generate_positions(report, len(promises))
    instr_queue = list()
    for prom in promises:
        rd = check_reg(prom.rd, register_matrix, report.reg_pool)
        rs1 = check_reg(prom.rs1, register_matrix, report.reg_pool)
        rs2 = check_reg(prom.rs2, register_matrix, report.reg_pool)
        instr = Instruction(prom.op.name.lower(), opcd_family[prom.op.name.lower()], r1=rd, r2=rs1, r3=rs2, immediate=prom.const)
        instr_queue.append(instr)
    for i in range(len(positions)):
        active_block = cfg.nodes[positions[i][0]]['block']
        for t in range(len(positions[i][1])):
            line = positions[i][1][t]
            instr = instr_queue[0]
            active_block.insert(line, instr)
            instr_queue.remove(instr)


def obfuscate(cfg: DiGraph, node_id: int, target_instr: int):
    instruction = cfg.nodes[node_id]["block"].pop(target_instr)
    max_shift = randint(0, 10)
    max_logical = randint(0, 10)
    promise_chain = generate_derivation_chain(instruction, max_shift, max_logical)
    needed_reg = calc_unresolved_register(promise_chain)
    report = calc_nodes_chain(cfg, node_id, target_instr, instruction.r1, needed_reg)
    placer(cfg, promise_chain, report)
