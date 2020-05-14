from networkx import DiGraph, neighbors
from structures import Register, not_modifiable_regs, opcodes
from rep.base import Instruction
from setup_structures import setup_contracts, organize_calls, sanitize_contracts
from registerbinder import bind_register_to_value
from random import randint


class NoUnusedRegsException(Exception):
    pass


class NoSubstitutionException(Exception):
    pass


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
    setup_contracts(cfg)
    sanitize_contracts(cfg)
    organize_calls(cfg)
    bind_register_to_value(cfg)

    node_id = list(cfg.nodes)[randint(1, len(cfg.nodes) - 1)]
    while 'external' in cfg.nodes[node_id]:
        node_id = list(cfg.nodes)[randint(1, len(cfg.nodes) - 1)]

    used_reg = find_used_reg(cfg, node_id)

    value_block = find_value_block(cfg, node_id, used_reg)

    if value_block is None:
        raise NoSubstitutionException

    try:
        unused_reg = find_unused_reg(cfg, node_id, heatmap, heat, value_block.initline, value_block.endline)
    except NoUnusedRegsException:
        raise NoSubstitutionException

    line_num = value_block.initline

    if isinstance(cfg.nodes[node_id]['block'][line_num], Instruction) and \
            cfg.nodes[node_id]['block'][line_num].r1 == used_reg:
        cfg.nodes[node_id]['block'][line_num].r1 = unused_reg

    line_num += 1

    switch_regs(line_num, value_block.endline, cfg.nodes[node_id], used_reg, unused_reg)

    setup_contracts(cfg)

    for node in cfg.nodes:
        bind_register_to_value(cfg, node)


def switch_regs(line_num: int, endline: int, current_node, used_register, unused_register):
    while line_num <= endline - 1:
        if isinstance(current_node['block'][line_num], Instruction):
            if current_node['block'][line_num].r1 == used_register:
                current_node['block'][line_num].r1 = unused_register
            if current_node['block'][line_num].r2 == used_register:
                current_node['block'][line_num].r2 = unused_register
            if current_node['block'][line_num].r3 == used_register:
                current_node['block'][line_num].r3 = unused_register
        line_num += 1

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


def get_requires_children(cfg: DiGraph, node_id: int):
    requires = set()
    for neigh in neighbors(cfg, node_id):
        for reg in cfg.nodes[neigh]['requires']:
            requires.add(reg)

    return requires


def find_value_block(cfg: DiGraph, node_id: int, used_reg: Register):
    value_blocks_qty = len(cfg.nodes[node_id]['reg_bind'][used_reg])
    requires_children = get_requires_children(cfg, node_id)

    while True:
        try:
            value_id = randint(0, value_blocks_qty - 1)
            if 0 < value_id < value_blocks_qty - 1:
                return cfg.nodes[node_id]['reg_bind'][used_reg][value_id]
            else:
                if value_id == 0:
                    if used_reg not in cfg.nodes[node_id]['requires']:
                        return cfg.nodes[node_id]['reg_bind'][used_reg][value_id]
                    else:
                        return None
                else:
                    if used_reg not in requires_children:
                        return cfg.nodes[node_id]['reg_bind'][used_reg][value_id]
                    else:
                        return None
        except ValueError:
            continue


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

    used_regs = list(reg for reg in cfg.nodes[current_node]['reg_bind'].keys() if reg not in not_modifiable_regs)
    unused_regs = list(reg for reg in Register if reg not in used_regs and reg not in not_modifiable_regs)
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
                print("Current node: {}".format(current_node))
                print("linea: {}".format(line))

    return chosen_unused
