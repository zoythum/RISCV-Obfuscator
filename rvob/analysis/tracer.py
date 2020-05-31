from typing import Mapping, List, Tuple

from networkx import DiGraph
from random import choice, seed
from itertools import count

from analysis.cfg import Transition, jump_ops, get_stepper
from rep.base import Instruction, ASMLine
from structures import Register, opcodes


def is_cond_jump(instr: Instruction) -> bool:
    if instr.opcode in jump_ops and jump_ops[instr.opcode] == Transition.C_JUMP:
        return True
    else:
        return False


def is_call(instr: Instruction) -> bool:
    if instr.opcode in jump_ops and jump_ops[instr.opcode] == Transition.CALL:
        return True
    else:
        return False


def line_register_heat(line: Instruction, max_heat: int, init: List[int]) -> List[int]:
    curr_heat = list(init)
    for reg in range(len(curr_heat)):
        if curr_heat[reg] > 0:
            curr_heat[reg] -= 1

        if opcodes[line.opcode][1]:
            curr_heat[line.r1.value] = max_heat
    return curr_heat


def get_new_execution(cfg: DiGraph, max_recursion: int):
    seed()
    line_counter = count(0)
    path_decision = []
    last_jump_line = 0
    heat_map = {}
    line_heat = [0] * len(Register)
    rec_counter = 0
    iterator = get_stepper(cfg, cfg.nodes[1]["block"].begin)
    for line in iterator:
        if line.number != -1 and isinstance(line.statement, Instruction):
            line_heat = line_register_heat(line.statement, 50, line_heat)
            heat_map[next(line_counter)] = line_heat
            if is_cond_jump(line.statement):
                decision: bool = False
                if last_jump_line != line.number:
                    rec_counter = 0
                    decision = choice([True, False])
                elif last_jump_line == line.number and rec_counter < max_recursion:
                    rec_counter += 1
                    decision = choice([True, False])
                elif last_jump_line == line.number and rec_counter == max_recursion:
                    rec_counter = 0
                    decision = False
                path_decision.append(decision)
                line = iterator.send(decision)
                line_heat = line_register_heat(line.statement, 50, line_heat)
                heat_map[next(line_counter)] = line_heat
            elif is_call(line.statement):
                if last_jump_line != line.number:
                    rec_counter = 0
                    last_jump_line = line.number
                elif last_jump_line == line.number and rec_counter < max_recursion:
                    rec_counter += 1
                elif last_jump_line == line.number and rec_counter == max_recursion:
                    break
    return path_decision, heat_map


def replay_execution(cfg: DiGraph, max_recursion: int, ex_path: List[bool]):
    seed()
    line_counter = count(0)
    path_decision = list(ex_path)
    last_jump_line = 0
    rec_counter = 0
    heat_map = {}
    line_heat = [0] * len(Register)
    iterator = get_stepper(cfg, cfg.nodes[1]["block"].begin)
    for line in iterator:
        if line.number != -1 and isinstance(line.statement, Instruction):
            line_heat = line_register_heat(line.statement, 50, line_heat)
            heat_map[next(line_counter)] = line_heat
            if is_cond_jump(line.statement):
                line = iterator.send(path_decision.pop(0))
                line_heat = line_register_heat(line.statement, 50, line_heat)
                heat_map[next(line_counter)] = line_heat
            elif is_call(line.statement):
                if last_jump_line != line.number:
                    rec_counter = 0
                    last_jump_line = line.number
                elif last_jump_line == line.number and rec_counter < max_recursion:
                    rec_counter += 1
                elif last_jump_line == line.number and rec_counter == max_recursion:
                    break

    return ex_path, heat_map


def get_trace(cfg: DiGraph, max_recursion: int = 5, ex_path: List[bool] = None) -> \
        Tuple[List[bool], Mapping[int, List[int]]]:
    if ex_path is None:
        return get_new_execution(cfg, max_recursion)
    else:
        return replay_execution(cfg, max_recursion, ex_path)
