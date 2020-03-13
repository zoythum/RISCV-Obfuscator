from networkx import DiGraph
from random import randint, choices
from setup_structures import get_free_regs
from structures import Register
from rep.instruction_generator import garbage_inst


def insert_garbage_instr(cfg: DiGraph, node: int = None, block_size: int = None):
    """
    This function adds a block of garbage instructions into a node of the graph
    @param cfg: the graph that represents the program
    @param node: the graph's node to which apply the function
    @param block_size: the number of garbage instructions that compose the block
    """
    if block_size is None:
        block_size = randint(1, 10)
    if node is None:
        node = randint(1, cfg.number_of_nodes())
    while 'external' in cfg.nodes[node]:
        node = randint(1, cfg.number_of_nodes())
    line_num = randint(cfg.nodes[node]["block"].begin, cfg.nodes[node]["block"].end - 1)
    free_regs = list(get_free_regs(cfg, line_num))
    all_regs = list(map(lambda r: r.name.lower(), Register))

    instr_list = choices(list(garbage_inst.keys()), k=block_size)
    for instr in instr_list:
        statement = garbage_inst[instr](free_regs, all_regs)
        cfg.nodes[node]["block"].insert(line_num, statement)
        line_num += 1
