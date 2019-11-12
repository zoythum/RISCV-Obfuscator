from networkx import DiGraph, shortest_path, neighbors
import random
from itertools import count


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
    while counter < len(nodes)-1:
        unmodifiable = find_unmodifiable_regs(cfg, counter, nodes)
        used_register, unused_register = find_valid_registers(cfg, counter)


def find_valid_registers(cfg: DiGraph, current_node) -> (int, int):
    used_regs = list(cfg.nodes[current_node]['reg_bind'].keys())
    try:
        used_regs.remove('ra')
    except ValueError:
        pass
    try:
        used_regs.remove('sp')
    except ValueError:
        pass
    chosen_used = used_regs[random.randint(0, len(used_regs))]

    return 0, 1


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
