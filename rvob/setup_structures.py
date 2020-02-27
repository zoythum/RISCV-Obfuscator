from networkx import DiGraph, neighbors, reverse, simple_cycles

from rep.base import Instruction
from rep.fragments import FragmentView
from rvob.structures import opcodes
from rvob.analysis import Transition
from structures import Register


def fill_contract(cfg: DiGraph, node_id: int):
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

    block: FragmentView = cfg.nodes[node_id]["block"]

    for i in range(block.get_end() - 1, block.get_begin() - 1, -1):
        current_line = block[i]
        if type(current_line) == Instruction:
            opcode = current_line.opcode
            r1 = current_line.r1
            r2 = current_line.r2
            r3 = current_line.r3
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

    # no need to keep 'unused' in our contracts
    if None in requires:
        requires.remove(None)
    if None in provides:
        requires.remove(None)

    # If the node we are dealing with is the return node of a function then it provides registers A0 and A1
    for edge in cfg.edges:
        data = cfg.get_edge_data(edge[0], edge[1])
        if edge[0] == node_id and data["kind"] == Transition.RETURN:
            provides.add(Register.A0)
            provides.add(Register.A1)

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


def setup_contracts(cfg: DiGraph):
    # TODO maybe we need to execute this function two times to take care of possible loops that are not
    #  satfisfied in the first iteration?
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
            fill_contract(cfg, node)
        except KeyError:
            continue
        for parent in reverse(cfg, False).neighbors(node):
            if parent not in remaining_nodes and parent not in visited:
                remaining_nodes.append(parent)

    sanitize_contracts(cfg)
    