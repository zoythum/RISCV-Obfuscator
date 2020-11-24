from typing import Dict, List

from networkx import DiGraph, neighbors
from structures import Register, not_modifiable_regs, opcodes
from rep.base import Instruction
from setup_structures import setup_contracts, organize_calls, sanitize_contracts
from registerbinder import bind_register_to_value, ValueBlock
from random import randint, choice, randrange
from rep.instruction_generator import mv_instr


class NoUnusedRegsException(Exception):
    pass


class NoSubstitutionException(Exception):
    pass


def setup(cfg: DiGraph):
    setup_contracts(cfg)
    sanitize_contracts(cfg)
    organize_calls(cfg)
    bind_register_to_value(cfg)


def split_value_blocks(cfg: DiGraph, heatmap, heat):
    setup(cfg)

    try:
        value_block, node_id, used_reg, unused_reg = get_scrambling_elements(cfg, heatmap, heat)
    except NoSubstitutionException:
        raise NoSubstitutionException

    try:
        line_num = randrange(value_block.init_line + 1, value_block.end_line)
    except ValueError:
        raise NoSubstitutionException

    mv_instruction = mv_instr([unused_reg], [used_reg])
    mv_instruction.original = used_reg
    mv_instruction.inserted = True
    mv_instruction.swap_instr = True

    cfg.nodes[node_id]['block'].insert(line_num, mv_instruction)
    line_num += 1
    switch_regs(line_num, value_block.end_line, cfg.nodes[node_id], used_reg, unused_reg)

    # ----------------Debugging Stuff Init------------------------ #
    print("###Done for splitting###")
    # ----------------Debugging Stuff End------------------------ #


def get_scrambling_elements(cfg: DiGraph, heatmap, heat):
    node_id = list(cfg.nodes)[randint(1, len(cfg.nodes) - 1)]
    count = 0
    value_block = None
    while value_block is None and count < int(len(list(cfg.nodes))*0.5):
        while 'external' in cfg.nodes[node_id]:
            node_id = choice(list(cfg.nodes))

        used_reg = find_used_reg(cfg, node_id)
        value_block = find_value_block(cfg, node_id, used_reg)
        count += 1

    if value_block is None:
        raise NoSubstitutionException

    try:
        unused_reg = find_unused_reg(cfg, node_id, heatmap, heat, value_block.init_line, value_block.end_line)
    except NoUnusedRegsException:
        raise NoSubstitutionException

    return value_block, node_id, used_reg, unused_reg


def substitute_reg(cfg: DiGraph, heatmap, heat):
    """
    Flow:
        1) estraggo nodo random
        2) estraggo registro usato e registro non usato
        3) estraggo blocco di validità
        4) sostituisco
    :param heatmap: generated heatmap for the current cfg
    :param heat: max heatmap's value
    :param cfg: cfg of the current program
    :return: void
    """
    setup(cfg)

    value_block, node_id, used_reg, unused_reg = get_scrambling_elements(cfg, heatmap, heat)
    line_num = value_block.init_line

    if isinstance(cfg.nodes[node_id]['block'][line_num], Instruction) and \
            cfg.nodes[node_id]['block'][line_num].r1 == used_reg:
        cfg.nodes[node_id]['block'][line_num].r1 = unused_reg

    line_num += 1

    switch_regs(line_num, value_block.end_line, cfg.nodes[node_id], used_reg, unused_reg)

    # ----------------Debugging Stuff Init------------------------ #
    print("###Done for substitute###")
    # ----------------Debugging Stuff End------------------------ #


def switch_regs(line_num: int, endline: int, current_node, used_register, unused_register):
    while line_num <= endline:
        if isinstance(current_node['block'][line_num], Instruction):
            instruction: Instruction = current_node['block'][line_num]
            if not opcodes[instruction.opcode][1] and instruction.r1 == used_register:
                instruction.r1 = unused_register
            if instruction.r2 == used_register:
                instruction.r2 = unused_register
            if instruction.r3 == used_register:
                instruction.r3 = unused_register
        line_num += 1
    if current_node['block'].end != line_num:
        fix_last_line(current_node, line_num, used_register, unused_register)


def fix_last_line(current_node, line_num, used_register, unused_register):
    if isinstance(current_node['block'][line_num], Instruction):
        if current_node['block'][line_num].r2 == used_register:
            current_node['block'][line_num].r2 = unused_register
        if current_node['block'][line_num].r3 == used_register:
            current_node['block'][line_num].r3 = unused_register

        if current_node['block'][line_num].r1 == used_register and \
                not opcodes[current_node['block'][line_num].opcode][1]:
            current_node['block'][line_num].r1 = unused_register


# def get_requires_children(cfg: DiGraph, node_id: int):
#     requires = set()
#     for neigh in neighbors(cfg, node_id):
#         for reg in cfg.nodes[neigh]['requires']:
#             requires.add(reg)
#
#     return requires


def find_value_block(cfg: DiGraph, node_id: int, used_reg: Register):
    value_blocks_qty = len(cfg.nodes[node_id]['reg_bind'][used_reg])

    for _ in range(100):
        try:
            value_id = randint(0, value_blocks_qty - 1)
            if cfg.nodes[node_id]['reg_bind'][used_reg][value_id].scrambled or \
                    cfg.nodes[node_id]['reg_bind'][used_reg][value_id].not_modify:
                continue
            else:
                return cfg.nodes[node_id]['reg_bind'][used_reg][value_id]
        except ValueError:
            continue

    return None


def find_used_reg(cfg: DiGraph, current_node) -> Register:
    """
    Retrieves two randomly selected registers, the first one such that is used in the current node while the second one
    is not used.
    :param heatmap: generated heatmap for the current cfg
    :param heat: max heatmap's value
    :param cfg: cfg of the current program
    :param current_node: current node where regs are searched
    :return: Register
    """

    used_regs = list(reg for reg in cfg.nodes[current_node]['reg_bind'].keys() if reg not in not_modifiable_regs)
    chosen_used = used_regs[randint(0, len(used_regs) - 1)]
    return chosen_used


def find_unused_reg(cfg: DiGraph, current_node, heatmap, heat, initline, endline) -> Register:
    """
    Retrieves two randomly selected registers, the first one such that is used in the current node while the second one
    is not used.
    :param value_block:
    :param heatmap: generated heatmap for the current cfg
    :param heat: max heatmap's value
    :param cfg: cfg of the current program
    :param current_node: current node where regs are searched
    :return: tuple of Register, first one is the used one, while the other one is the unused
    """
    reg_binder: Dict[Register, List[ValueBlock]] = cfg.nodes[current_node]['reg_bind']
    used_regs = list(reg for reg in cfg.nodes[current_node]['reg_bind'].keys() if reg not in not_modifiable_regs)
    unused_regs = list(reg for reg in Register if reg not in not_modifiable_regs)

    for reg in used_regs:
        for elem in reg_binder[reg]:
            if initline <= elem.init_line <= endline or initline <= elem.end_line <= endline:
                unused_regs.remove(reg)
                break

    min_heat = heat

    if len(unused_regs) == 0:
        raise NoUnusedRegsException

    try:
        heatmap[initline][0]
    except KeyError:
        return unused_regs[randint(0, len(unused_regs) - 1)]

    chosen_unused = unused_regs[0]

    for line in range(initline, endline):
        for un_reg in unused_regs:
            try:
                if heatmap[line][un_reg.value] < min_heat:
                    chosen_unused = un_reg
                    min_heat = heatmap[line][un_reg.value]
            except KeyError:
                pass

    return chosen_unused
