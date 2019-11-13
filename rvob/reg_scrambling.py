from networkx import DiGraph, shortest_path, neighbors
from rvob.structures import opcodes
from rvob.rep.base import Instruction
import random


def substitute_reg(cfg: DiGraph):
    # first we generate two random numbers which identify the two node defining the branch of the tree in which
    # we are going to change the registers
    initial_id = random.randint(1, len(cfg.nodes) - 2)
    try:
        final_id = random.randint(initial_id + 1, len(cfg.nodes) - 2)
    except ValueError:
        return
    nodes = shortest_path(cfg, initial_id, final_id)
    counter = 0
    while counter < len(nodes) - 1:
        unmodifiable = find_unmodifiable_regs(cfg, counter, nodes)
        used_register, unused_register = find_valid_registers(cfg, counter, unmodifiable)
        used_values = cfg.nodes[counter]['reg_bind'][used_register][random
            .randint(0, len(cfg.nodes[counter]['reg_bind'][used_register]))]
        line_num = used_values.initline
        cfg.nodes[counter]['block'].insert(line_num-1, "mv " + unused_register + " " + used_register)

        # For each line in which the used_reg contains the same value we operate a switch of registers
        # checking each register
        while line_num < used_values.endline:

            if type(cfg.nodes[counter]['block'][line_num]) is Instruction:

                if cfg.nodes[counter]['block'][line_num]['r1'] == used_register:
                    cfg.nodes[counter]['block'][line_num]['r1'] = unused_register
                if cfg.nodes[counter]['block'][line_num]['r2'] == used_register:
                    cfg.nodes[counter]['block'][line_num]['r2'] = unused_register
                if cfg.nodes[counter]['block'][line_num]['r3'] == used_register:
                    cfg.nodes[counter]['block'][line_num]['r3'] = unused_register

            line_num += 1
        counter += 1


def find_valid_registers(cfg: DiGraph, current_node, unmodifiable) -> (int, int):
    # Given a DiGraph and a node_id this function randomly choses a tuple of registers, the first one is a register used
    # in the node and the other is an unused register. During the selection of the used one we keep track of the
    # unmodifiable registers
    used_regs = list(cfg.nodes[current_node]['reg_bind'].keys())

    unused_regs = list(opcodes)
    for reg in used_regs:
        unused_regs.remove(reg)

    for unmod_reg in unmodifiable:
        if unmod_reg in used_regs:
            used_regs.remove(unmod_reg)
    try:
        used_regs.remove('ra')
    except ValueError:
        pass
    try:
        used_regs.remove('sp')
    except ValueError:
        pass

    chosen_used = used_regs[random.randint(0, len(used_regs))]
    chosen_unused = unused_regs[random.randint(0, len(unused_regs))]
    return chosen_used, chosen_unused


def find_unmodifiable_regs(cfg: DiGraph, current_node, nodes) -> set:
    # We need to find which registers can't be modified at all, those are all the register that can be found in
    # a requires set of a neighbor of the current node if two properties are verified:
    # 1) the neighbor we are considering is not part of the chosen path
    # 2) the register we are considering doesn't appear in the provides set of the current node
    unmodifiable = set()
    for neigh in neighbors(cfg, current_node):
        if neigh not in nodes:
            for reg in cfg.nodes[neigh]['requires']:
                if reg not in cfg.nodes[current_node]['provides']:
                    unmodifiable.add(reg)

    return unmodifiable
