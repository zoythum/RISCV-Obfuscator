from typing import Mapping, List, Tuple, Dict

from networkx import DiGraph
from random import choice, seed
from itertools import count

from analysis.cfg import Transition, jump_ops, get_stepper
from rep.base import Instruction
from structures import Register, opcodes


class SupplementInfo:
    """
    an element that contains some additional info about a certain line of code, the inserted attribute is True if the
    associated instruction is inserted by some obfuscation technic, otherwise is False. The o_reg attribute contains the
    original writing register used by the instruction, if any, otherwise is set to None, the n_reg attribute contains
    the actual write register, if any, None otherwise.
    """
    def __init__(self, inserted, o_reg, n_reg):
        self.inserted = inserted
        self.o_reg = o_reg
        self.n_reg = n_reg


def is_cond_jump(instr: Instruction) -> bool:
    """
    check if the given instruction represent a conditional jump
    @param instr: the instruction to be inspected
    @return: true if the instruction is a conditional branch one, false otherwise
    """
    if instr.opcode in jump_ops and jump_ops[instr.opcode] == Transition.C_JUMP:
        return True
    else:
        return False


def is_call(instr: Instruction) -> bool:
    """
    check if the given instruction is a CALL instruction
    @param instr: the instruction to be inspected
    @return: true if the instruction is a call, false otherwise
    """
    if instr.opcode in jump_ops and jump_ops[instr.opcode] == Transition.CALL:
        return True
    else:
        return False


def line_register_heat(line: Instruction, max_heat: int, init: List[int]) -> List[int]:
    """
    calculate the heat of the given line. The calculation is based on the given initialization vector
    @param line: the to of which we want to calculate the heat
    @param max_heat: the maximum heat that can be associated to a register
    @param init: the initialization vector
    @return: the heat vector of the given line
    """
    curr_heat = list(init)
    for reg in range(len(curr_heat)):
        if curr_heat[reg] > 0:
            curr_heat[reg] -= 1

        if opcodes[line.opcode][1]:
            curr_heat[line.r1.value] = max_heat
    return curr_heat


def compute_additional_info(line: Instruction):
    """
    This function extrapolate the additional information required for the obfuscation technics evaluation, it check if
    the instruction is an original one or if it's inserted by some technic and then took the original write register and
    the actual one, if the first register is used as a destination register
    @param line: the instruction under analysis
    @return: a SupplementInfo element
    """
    if line.original is None:
        return SupplementInfo(line.inserted, None, None)
    else:
        if isinstance(line.original, Register):
            return SupplementInfo(line.inserted, line.original.name, line.r1.name)
        else:
            return SupplementInfo(line.inserted, line.original.upper(), line.r1.name)


def get_new_execution(cfg: DiGraph, max_recursion: int):
    """
    simulate a casual execution of the program starting from it's cfg.
    @param cfg: the program's cfg
    @param max_recursion: the maximum accepted recursion deep
    @return: a tuple where in the first position there is the list of the branching's decisions and the second element
             is the heat-map associated to the execution
    """
    seed()
    line_counter = count(0)
    path_decision = []
    last_jump_line = 0
    exec_data = {}
    line_heat = [0] * len(Register)
    rec_counter = 0
    iterator = get_stepper(cfg, cfg.nodes[1]["block"].begin)
    for line in iterator:
        if line.number != -1 and isinstance(line.statement, Instruction):
            line_heat = line_register_heat(line.statement, 50, line_heat)
            exec_data[next(line_counter)] = (line_heat, compute_additional_info(line.statement))
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
                exec_data[next(line_counter)] = (line_heat, compute_additional_info(line.statement))
            elif is_call(line.statement):
                if last_jump_line != line.number:
                    rec_counter = 0
                    last_jump_line = line.number
                elif last_jump_line == line.number and rec_counter < max_recursion:
                    rec_counter += 1
                elif last_jump_line == line.number and rec_counter == max_recursion:
                    break
    return path_decision, exec_data


def replay_execution(cfg: DiGraph, max_recursion: int, ex_path: List[bool]):
    """
    simulate the execution of the program basing it's branching decision on the given decision's list
    @param cfg: the program cfg
    @param max_recursion: the maximum accepted recursion deep
    @param ex_path: the list of the decision that must be took at the branching point to obtain the desired execution
    @return: a tuple where in the first position there is the list of the branching's decisions and the second element
             is the heat-map associated to the execution
    """
    seed()
    line_counter = count(0)
    path_decision = list(ex_path)
    last_jump_line = 0
    rec_counter = 0
    exec_data = {}
    line_heat = [0] * len(Register)
    iterator = get_stepper(cfg, cfg.nodes[1]["block"].begin)
    for line in iterator:
        if line.number != -1 and isinstance(line.statement, Instruction):
            line_heat = line_register_heat(line.statement, 50, line_heat)
            exec_data[next(line_counter)] = (line_heat, compute_additional_info(line.statement))
            if is_cond_jump(line.statement):
                line = iterator.send(path_decision.pop(0))
                line_heat = line_register_heat(line.statement, 50, line_heat)
                exec_data[next(line_counter)] = (line_heat, compute_additional_info(line.statement))
            elif is_call(line.statement):
                if last_jump_line != line.number:
                    rec_counter = 0
                    last_jump_line = line.number
                elif last_jump_line == line.number and rec_counter < max_recursion:
                    rec_counter += 1
                elif last_jump_line == line.number and rec_counter == max_recursion:
                    break

    return ex_path, exec_data


def get_trace(cfg: DiGraph, max_recursion: int = 5, ex_path: List[bool] = None) -> \
        Tuple[List[bool], Dict[int, Tuple[List[int], SupplementInfo]]]:
    """
    This function simulate an execution returning the heat-map associated to the execution paired with the decision
    taken at the conditional branching point. Or, if the list of the decision taken is passed, could replay a past
    execution of the same program
    @param cfg: the cfg of the program
    @param max_recursion: the maximum recursion deep accepted, by default is set to 5
    @param ex_path: the list of decision that must be taken at the branching point
    @return: a tuple where in the first position there is the list of the branching's decisions and the second element
             is the heat-map associated to the execution
    """
    if ex_path is None:
        return get_new_execution(cfg, max_recursion)
    else:
        return replay_execution(cfg, max_recursion, ex_path)
