from networkx import DiGraph
from random import randint, choices
from analysis import free_regs_at
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
    line_num = randint(cfg.nodes[node]["block"].begin, cfg.nodes[node]["block"].end - 1)
    free_regs = list(free_regs_at(line_num - 1, cfg))
    all_regs = list(map(lambda r: r.name.lower(), Register))

    instr_list = choices(list(garbage_inst.keys()), k=block_size)
    for instr in instr_list:
        statement = garbage_inst[instr](free_regs, all_regs)
        cfg.nodes[node]["block"].insert(line_num, statement)
        line_num += 1
