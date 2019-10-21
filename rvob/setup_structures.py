###
# TODO never do this
from networkx import *
###
import rvob.transform as transform
import rvob.rep as rep
import json


# TODO node_id is int
def fill_contract(cfg: DiGraph, node_id: str, src: rep.Source):
    # Function that creates the contract for a single node, we use two different sets:
    # 1) provides contains all the registers written in this node's code block
    # 2) requires contains all the registers that are read in this node's code block
    # Initially requires set contains all the registers in the requires sets of the node's children, each time that a
    # register is written is also removed from the set, otherwise if a register is written then we add it to the set
    provides = set()
    requires = set()
    children = get_children(cfg, node_id)
    for child in children:
        for elem in cfg.nodes[child]["requires"]:
            requires.add(elem)

    # TODO remove spaghetti
    inizio = cfg.nodes[int(node_id)]["start"]
    fine = cfg.nodes[int(node_id)]["end"]

    # TODO no need to cast
    for i in range(int(fine), int(inizio) - 1, -1):
        current_line = src.lines[i]
        if type(current_line) == rep.Instruction:
            r1 = current_line.instr_args['r1']
            r2 = current_line.instr_args['r2']
            r3 = current_line.instr_args['r3']
            # TODO sets are add-invariant
            if r1 not in provides:
                provides.add(r1)
            if r1 in requires:
                requires.remove(r1)
            if r2 not in requires:
                requires.add(r2)
            if r3 not in requires:
                requires.add(r3)

    # no need to keep unused and reg_err (which should not appear anyway) in our contracts
    if 'unused' in requires:
        requires.remove('unused')
    if 'unused' in provides:
        requires.remove('unused')
    # TODO raise exception when reg_err
    if 'reg_err' in requires:
        requires.remove('reg_err')
    if 'reg_err' in provides:
        requires.remove('reg_err')

    cfg.nodes[node_id]['requires'] = requires
    cfg.nodes[node_id]['provides'] = provides


def get_children(cfg: DiGraph, node_id: str):
    # Utility function, recovers the children of a specific node, if the head of the tree should appear as a child it
    # will be ignored
    children = []
    # TODO check if neighbors returns parents too
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
    # TODO what is this shadowing?
    cycles = list(simple_cycles(cfg))

    for elem in list(cycles):
        if 0 in elem:
            cycles.remove(elem)

    for elem in list(cycles):
        for elem2 in list(cycles):
            if is_sublist(elem, elem2):
                print(elem)
                cycles.remove(elem)

    # TODO remove this debug print
    print(cycles)

    for cycle in cycles:
        req = cfg.nodes[cycle[0]]['requires']
        for node in cycle:
            cfg.nodes[node]['requires'] = req


def setup_contracts():
    # TODO remove this testing/debugging code
    file = open("aes.json")
    src = rep.load_src(json.load(file))
    cfg = transform.build_cfg(src)
    for i in range(0, len(cfg.nodes)):
        cfg.nodes[i]['provides'] = set()
        cfg.nodes[i]['requires'] = set()
    # Recovers the leaves of our tree
    # TODo there are no nodes that satisfy this condition
    remaining_nodes = [x for x in cfg.nodes() if cfg.out_degree(x) == 0 and cfg.in_degree(x) == 1]
    # TODO convert to a set
    visited = []
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
        visited.append(node)
        try:
            # We need to check if the node we're dealing with has a start attribute, otherwise we ignore the node and
            # skip to the next one (should happen only at the end when dealing with the head of the cfg)
            # TODO exception originates from the called function already
            cfg.nodes[node]['start']
            fill_contract(cfg, node, src)
        except KeyError:
            continue
        for parent in reverse(cfg, False).neighbors(node):
            if parent not in remaining_nodes and parent not in visited:
                remaining_nodes.append(parent)

    sanitize_contracts(cfg)


# TODO remove this top-level statement, use the console
setup_contracts()
