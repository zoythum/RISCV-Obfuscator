from networkx import DiGraph, neighbors
from structures import Register, not_modifiable_regs, opcodes
from rep.base import Instruction
from setup_structures import setup_contracts
from registerbinder import bind_register_to_value
from random import randint


def substitute_reg(cfg: DiGraph):
    """
    Flow:
        1) estraggo nodo random
        2) estraggo registro usato e registro non usato
        3) estraggo blocco di validità
        4) sostituisco
    :param cfg:
    :return:
    """

    node_id = list(cfg.nodes)[randint(1, len(cfg.nodes) - 1)]
    while 'external' in cfg.nodes[node_id]:
        node_id = list(cfg.nodes)[randint(1, len(cfg.nodes) - 1)]

    used_reg, unused_reg = find_valid_registers(cfg, node_id)

    value_block = find_value_block(cfg, node_id, used_reg)

    if value_block is None:
        return

    line_num = value_block.initline

    if isinstance(cfg.nodes[node_id]['block'][line_num], Instruction) and \
            cfg.nodes[node_id]['block'][line_num].r1 == used_reg:
        cfg.nodes[node_id]['block'][line_num].r1 = unused_reg

    line_num += 1

    switch_regs(line_num, value_block.endline, cfg.nodes[node_id], used_reg, unused_reg, node_id)

    setup_contracts(cfg)
    for node in cfg.nodes:
        bind_register_to_value(cfg, node)


def switch_regs(line_num: int, endline: int, current_node, used_register, unused_register, node_id):

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


def find_valid_registers(cfg: DiGraph, current_node) -> (Register, Register):
    """
    Retrieves two randomly selected registers, the first one such that is used in the current node while the second one
    is not used.
    :param cfg:
    :param current_node:
    :return:
    """

    used_regs = list(reg for reg in cfg.nodes[current_node]['reg_bind'].keys() if reg not in not_modifiable_regs)
    unused_regs = list(reg for reg in Register if reg not in used_regs and reg not in not_modifiable_regs)
    chosen_used = used_regs[randint(0, len(used_regs) - 1)]
    chosen_unused = unused_regs[randint(0, len(unused_regs) - 1)]
    return chosen_used, chosen_unused
