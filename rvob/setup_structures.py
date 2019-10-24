from networkx import DiGraph, neighbors, reverse, simple_cycles
import rvob.rep as rep


# This is a classification of all the possible opcodes.
# Each opcode is paired with a tuple (<int>, <boolean>) where the int value represents the number of registers used
# by that specific opcode, the boolean value instead tells if we are dealing with a write function (True)
# or a read only one (False)
opcodes = {
    'lui': (1, True), 'auipc': (1, True), 'jal': (1, True), 'jalr': (2, True), 'lb': (2, True), 'lh': (2, True),
    'lw': (2, True), 'lbu': (2, True), 'lhu': (2, True), 'addi': (2, True), 'slti': (2, True),
    'sltiu': (2, True), 'xori': (2, True), 'ori': (2, True), 'andi': (2, True), 'slli': (2, True),
    'srli': (2, True), 'srai': (2, True), 'lwu': (2, True), 'ld': (2, True), 'addiw': (2, True),
    'slliw': (2, True), 'srliw': (2, True), 'sext.w': (2, True), 'mv': (2, True), 'sraiw': (2, True), 'lr.w': (2, True),
    'lr.d': (2, True), 'add': (3, True), 'sub': (3, True), 'sll': (3, True), 'slt': (3, True),
    'sltu': (3, True), 'xor': (3, True), 'srl': (3, True), 'sra': (3, True), 'or': (3, True), 'and': (3, True),
    'addw': (3, True), 'subw': (3, True), 'sllw': (3, True), 'srlw': (3, True), 'sraw': (3, True), 'mul': (3, True),
    'mulh': (3, True), 'mulhsu': (3, True), 'div': (3, True), 'divu': (3, True), 'rem': (3, True),
    'remu': (3, True), 'mulw': (3, True), 'divw': (3, True), 'divuw': (3, True), 'remw': (3, True),
    'remuw': (3, True), 'sc.w': (3, True), 'amoswap.w': (3, True), 'amoadd.w': (3, True),
    'amoxor.w': (3, True), 'amoor.w': (3, True), 'amoand.w': (3, True), 'amomin.w': (3, True), 'amomax.w': (3, True),
    'amominu.w': (3, True), 'amomaxu.w': (3, True), 'sc.d': (3, True), 'amoswap.d': (3, True), 'amoadd.d': (3, True),
    'amoxor.d': (3, True), 'amoor.d': (3, True), 'amoand.d': (3, True), 'amomin.d': (3, True),
    'amomax.d': (3, True), 'amominu.d': (3, True), 'amomaxu.d': (3, True), 'jr': (1, False), 'j': (1, False),
    'beq': (2, False), 'bne': (2, False), 'blt': (2, False), 'bge': (2, False), 'ble': (2, False), 'bltu': (2, False),
    'bgeu': (2, False), 'sb': (2, False), 'sh': (2, False), 'sw': (2, False), 'sd': (2, False), 'li': (1, True),
    'beqz': (1, False), 'bnez': (1, False), 'bgtu': (2, False), 'bleu': (2, False), 'nop': (0, False)
}


def fill_contract(cfg: DiGraph, node_id: int, src: rep.Source):
    # Function that creates the contract for a single node, we use two different sets:
    # 1) provides contains all the registers written in this node's code block
    # 2) requires contains all the registers that are read in this node's code block
    # Initially requires set contains all the registers in the requires sets of the node's children, each time that a
    # register is written is also removed from the set, otherwise if a register is written then we add it to the set
    provides = set()
    requires = set()
    errors = set()
    children = get_children(cfg, node_id)
    for child in children:
        for elem in cfg.nodes[child]["requires"]:
            requires.add(elem)

    start = cfg.nodes[node_id]["start"]
    end = cfg.nodes[node_id]["end"]

    for i in range(end, start - 1, -1):
        current_line = src.lines[i]
        if type(current_line) == rep.Instruction:
            opcode = current_line.opcode
            r1 = current_line.instr_args['r1']
            r2 = current_line.instr_args['r2']
            r3 = current_line.instr_args['r3']
            # Different actions are taken depending on the type of opcode we are analizing, if we have a read only
            # opcode provides set will not be modified, otherwise we make sure to deal with that set too
            if opcode in opcodes.keys():
                if opcodes[opcode][1]:
                    provides.add(r1)
                    if r1 in requires:
                        requires.remove(r1)
                    if r2 not in requires:
                        requires.add(r2)
                    if r3 not in requires:
                        requires.add(r3)
                else:
                    if r1 not in requires:
                        requires.add(r1)
                    if r2 not in requires:
                        requires.add(r2)
                    if r3 not in requires:
                        requires.add(r3)
            else:
                errors.add(opcode)

    # A little bit of error management, if we have some opcodes that are not classified is better to raise an exception
    # instead of ignoring them and having to deal with bigger problems later
    if len(errors) > 0:
        raise Exception("Encountered one or more unexpected opcodes, {}".format(errors))

    # no need to keep unused and reg_err (which should not appear anyway) in our contracts
    if 'unused' in requires:
        requires.remove('unused')
    if 'unused' in provides:
        requires.remove('unused')
    if 'reg_err' in requires or 'reg_err' in provides:
        raise Exception("Reg_err found in requires/provides set")

    cfg.nodes[node_id]['requires'] = requires
    cfg.nodes[node_id]['provides'] = provides


def get_children(cfg: DiGraph, node_id: int):
    # Utility function, recovers the children of a specific node, if the head of the tree should appear as a child it
    # will be ignored
    children = []
    for child in neighbors(cfg, node_id):
        children.append(child)
    if 0 in children:
        children.remove(0)
    return children


def is_sublist(sublist: list, main_list: list):
    # Utility functions, given two strings checks if the first one is totally contained in the second one
    if len(sublist) >= len(main_list):
        return False
    else:
        for elem in sublist:
            if elem not in main_list:
                return False
    return True


def sanitize_contracts(cfg: DiGraph):
    # This function sanitizes all the contracts, firstly it finds all the cycles in the graph, then
    # it copies the cycle head's "requires" contract into each node of the cycle
    cycles = list(simple_cycles(cfg))

    for elem in list(cycles):
        if 0 in elem:
            cycles.remove(elem)

    for elem in list(cycles):
        for elem2 in list(cycles):
            if is_sublist(elem, elem2):
                print(elem)
                cycles.remove(elem)

    for cycle in cycles:
        req = cfg.nodes[cycle[0]]['requires']
        for node in cycle:
            cfg.nodes[node]['requires'] = req


def setup_contracts(src: rep.Source, cfg: DiGraph):
    for i in range(0, len(cfg.nodes)):
        cfg.nodes[i]['provides'] = set()
        cfg.nodes[i]['requires'] = set()
    # Recovers the leaves of our tree
    remaining_nodes = []
    visited = set()
    # Adds all the nodes that are leaves but were previously filtered out because of a connection with the head of
    # the tree (wich should be all the leaves because of the way in wich we create the tree in the first place)
    for node in reverse(cfg, False).neighbors(0):
        if cfg.out_degree(node) == 1:
            remaining_nodes.append(node)

    # Core loop of the function, its behaviour is:
    # 1) check if we still have nodes that need to be analyzed, if not end
    # 2) pop the first node of the stack, put it in the visited list, create the contract for this node.
    # 3) recover its parent node and if it's not in the stack and it has never been visited append it to the stack
    # 4) start from point 1
    while len(remaining_nodes) > 0:
        node = remaining_nodes.pop(0)
        visited.add(node)
        try:
            # We need to check if the node we're dealing with has a start attribute, otherwise we ignore the node and
            # skip to the next one (should happen only at the end when dealing with the head of the cfg)
            fill_contract(cfg, node, src)
        except KeyError:
            continue
        for parent in reverse(cfg, False).neighbors(node):
            if parent not in remaining_nodes and parent not in visited:
                remaining_nodes.append(parent)

    sanitize_contracts(cfg)

