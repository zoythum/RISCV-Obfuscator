from networkx import DiGraph, neighbors, reverse, simple_cycles
import rvob.rep as rep


def fill_contract(cfg: DiGraph, node_id: int, src: rep.Source):
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

    start = cfg.nodes[node_id]["start"]
    end = cfg.nodes[node_id]["end"]

    for i in range(end, start - 1, -1):
        current_line = src.lines[i]
        if type(current_line) == rep.Instruction:
            r1 = current_line.instr_args['r1']
            r2 = current_line.instr_args['r2']
            r3 = current_line.instr_args['r3']

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
    if 'reg_err' in requires or 'reg_err' in provides:
        raise Exception("Reg_err found in requires/provides set")

    cfg.nodes[node_id]['requires'] = requires
    cfg.nodes[node_id]['provides'] = provides


def get_children(cfg: DiGraph, node_id: int):
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


