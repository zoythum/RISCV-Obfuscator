from networkx import DiGraph, shortest_path, neighbors
from rvob.structures import registers
from rvob.rep.base import Instruction
from rvob.setup_structures import setup_contracts
from rvob.registerbinder import bind_register_to_value
from random import randint


def substitute_reg(cfg: DiGraph):

    try:
        final_id = randint(1, len(cfg.nodes) - 1)
    except ValueError:
        return

    # To avoid situations where the shortest path uses the root of the tree (since each leaf is connected to the root)
    # we find the shortest path from the root itself to a randomly chosen id. Then an intermediate
    # value that will be our initial_id is selected and the final path is obtained removing each node
    # from 0 to inital_id
    nodes = shortest_path(cfg, 0, final_id)
    initial_id = nodes[randint(0, len(nodes)-2)]
    while nodes[0] != initial_id:
        nodes.pop(0)

    counter = initial_id

    while counter < final_id:
        extended = False
        current_node = cfg.nodes[counter]
        unmodifiable = find_unmodifiable_regs(cfg, counter, nodes)
        used_register, unused_register = find_valid_registers(cfg, counter, unmodifiable)
        # requires_other is a set that contains all the registers that are required by blocks that are not part of the
        # path we are analyzing
        requires_other = set()
        for neigh in neighbors(cfg, counter):
            if neigh not in nodes:
                for reg in cfg.nodes[neigh]['requires']:
                    requires_other.add(reg)

        # In different parts of a block in a register we can find different values, each of those values is saved
        # in the reg_bind structure. To obfuscate we randomly chose a value, whose id is saved in value_id
        if used_register in unmodifiable:
            # TODO da rivedere questo randint, può dare errore
            try:
                value_id = randint(1, len(current_node['reg_bind'][used_register]) - 2)
            except ValueError:
                return
            used_values = current_node['reg_bind'][used_register][value_id]
        else:
            value_id = randint(0, len(current_node['reg_bind'][used_register]) - 1)
            used_values = current_node['reg_bind'][used_register][value_id]

        # If the used_register we chose is required from one of the blocks
        if used_register in current_node['provides'] and used_register in requires_other:
            current_node['block'].insert(current_node['block'].get_begin() + used_values.endline, "mv "
                                         + used_register + " " + unused_register)

        if value_id == randint(0, len(current_node['reg_bind'][used_register]) - 1) and \
                used_register in cfg.nodes[counter + 1]['requires']:
            if len(list(cfg.predecessors(counter + 1))) > 1:
                # Our child has more than one parent, we can't be sure that the value we are considering is preserved
                # in the next block so better ignore and move on
                counter += 1
                continue
            else:
                # Otherwise we know that the first value we are encountering in the next block is the same as this one
                extended = True

        line_num = used_values.initline

        if type(current_node['block'][line_num]) is Instruction and \
                current_node['block'][line_num]['r1'] == used_register:
            current_node['block'][line_num]['r1'] = unused_register

        # For each line in which the used_reg contains the same value we operate a switch of registers
        # checking each register
        switch_regs(line_num, used_values.endline, current_node, used_register, unused_register)
        if extended:
            # If the value continues in the next block we must change also the next value
            # TODO potrebbe esserci un problema qui, perché?
            used_values = cfg.nodes[counter + 1]['reg_bind'][used_register][0]
            switch_regs(used_values.initline, used_values.endline, cfg.nodes[counter + 1], used_register,
                        unused_register)
        counter += 1

        setup_contracts(cfg)
        bind_register_to_value(cfg)


def switch_regs(line_num: int, endline: int, current_node, used_register, unused_register):
    while line_num < endline:
        # todo modifica seguendo cambio tomas
        if type(current_node['block'][line_num]) is Instruction:
            if current_node['block'][line_num]['r1'] == used_register:
                current_node['block'][line_num]['r1'] = unused_register
            if current_node['block'][line_num]['r2'] == used_register:
                current_node['block'][line_num]['r2'] = unused_register
            if current_node['block'][line_num]['r3'] == used_register:
                current_node['block'][line_num]['r3'] = unused_register

        line_num += 1


def find_valid_registers(cfg: DiGraph, current_node, unmodifiable) -> (int, int):
    # Given a DiGraph and a node_id this function randomly choses a tuple of registers, the first one is a register used
    # in the node and the other is an unused register. During the selection of the used one we keep track of the
    # unmodifiable registers
    used_regs = list(cfg.nodes[current_node]['reg_bind'].keys())
    
    unused_regs = list(registers)

    for reg in used_regs:
        unused_regs.remove(reg)

    unused_regs.remove('unused')
    unused_regs.remove('reg_err')
    # for unmod_reg in unmodifiable:
    #     if unmod_reg in used_regs:
    #         used_regs.remove(unmod_reg)

    chosen_used = used_regs[randint(0, len(used_regs) - 1)]

    chosen_unused = unused_regs[randint(0, len(unused_regs) - 1)]
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
