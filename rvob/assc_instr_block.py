from typing import Tuple, Dict, List

from networkx import DiGraph

from structures import opcodes
from rep.base import Instruction
from rvob.registerbinder import ValueBlock, populate_linelist
from structures import Register


def search_correspondance(line: int, blocks: List[ValueBlock]) -> int:
    for el in blocks:
        if el.initline <= line <= el.endline:
            if isinstance(el.group_id, Instruction):
                print()
            return el.group_id


def retrieve_instr_group_ids(ln_tp: Tuple[int, Instruction], reg_bind: Dict[Register, List[ValueBlock]]):
    instr = ln_tp[1]
    if instr.r1 is not None:
        instr.group_id[0] = search_correspondance(ln_tp[0], reg_bind[instr.r1])
        if isinstance(instr.group_id[0], Instruction):
            print("Errore")
    else:
        return
    if instr.r2 is not None:
        instr.group_id[1] = search_correspondance(ln_tp[0], reg_bind[instr.r2])
    else:
        return
    if instr.r3 is not None:
        instr.group_id[2] = search_correspondance(ln_tp[0], reg_bind[instr.r3])
    else:
        return


def init_group_ids(cfg: DiGraph):
    for nd_id in cfg.nodes:
        if 'external' not in cfg.nodes[nd_id]:
            reg_bind: Dict[Register, List[ValueBlock]] = cfg.nodes[nd_id]['reg_bind']
            for val in reg_bind.values():
                for el in val:
                    el.group_id = el.value


def associate_instruction_to_ValueBlock(cfg: DiGraph):
    init_group_ids(cfg)
    for nd_id in cfg.nodes:
        node = cfg.nodes[nd_id]
        if 'external' not in node:
            reg_bind = node['reg_bind']
            lines = populate_linelist(cfg, nd_id)
            for ln_tp in lines:
                if isinstance(ln_tp[1], Instruction):
                    retrieve_instr_group_ids(ln_tp, reg_bind)


def search_for_write(reg_bind: Dict[Register, List[ValueBlock]]) -> int:
    max_value = 0
    for val in reg_bind.values():
        for el in val:
            if el.group_id > max_value:
                max_value = el.group_id
    return max_value + 1


def search_for_read(node: DiGraph.node, reg: Register, line: int) -> int:
    index = line - 1
    while index >= node['block'].begin:
        statement = node['block'][index]
        if isinstance(statement, Instruction) and opcodes[statement.opcode][1] and reg.name == statement.r1.name:
            return statement.group_id[0]
        index -= 1
    return index


def call_ids_new_instr(cfg: DiGraph, node: int, instr: Instruction, line: int):
    if opcodes[instr.opcode][1]:
        instr.group_id[0] = search_for_write(cfg.nodes[node]['reg_bind'])
    else:
        if instr.r1 is not None:
            instr.group_id[0] = search_for_read(cfg.nodes[node], instr.r1, line)
        else:
            return
    if instr.r2 is not None:
        instr.group_id[1] = search_for_read(cfg.nodes[node], instr.r2, line)
    else:
        return
    if instr.r3 is not None:
        instr.group_id[2] = search_for_read(cfg.nodes[node], instr.r3, line)
    else:
        return
