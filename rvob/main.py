import json
from sys import argv, exit
from rvob.rep.fragments import load_src_from_maps
from rvob.analysis.cfg import build_cfg
from rvob.setup_structures import setup_contracts, organize_calls, sanitize_contracts
from rvob.registerbinder import bind_register_to_value
from rvob.garbage_inserter import insert_garbage_instr
from rvob.obf.obfuscator import obfuscate
from rvob.scrambling import substitute_reg
from rvob.analysis.heatmaps import register_heatmap
from rvob.rep.base import to_line_iterator
from random import randint


def get_immediate_instructions(cfg):
    """
    returns a list of tuples where the first parameter represents a node and the second one is a line number.
    Those tuples defines all the immediate instructions found in the specified cfg
    :param cfg:
    :return: list[(node, line_num)]
    """
    result = []
    for node in cfg.nodes:
        if "external" not in cfg.nodes[node]:
            current_node = cfg.nodes[node]
            iterator = to_line_iterator(current_node['block'].iter(current_node['block'].begin),
                                        current_node['block'].begin)
            while True:
                try:
                    line = iterator.__next__()
                    line_num = line.number
                    stat = line.statement
                    if stat.family == "i" and stat.ImmediateConstant is None:
                        result.append((node, line_num))
                except StopIteration:
                    break
    return result


def main():
    if len(argv) < 2:
        print("Missing parameters, try -h for usage informations")
        exit(1)

    if len(argv) == 2 and argv[1] == "-h":
        print("Usage informations:")
        print("{} \"path/to/json\" \"cfg entry point\" \"repetition value\" \"heat value\" \"path/to/output\""
              .format(argv[0]))
        exit(1)
    elif 2 < len(argv) < 6:
        print("Missing parameters, try -h for usage informations")
        exit(1)
    elif len(argv) == 6:
        print(argv[1])
        file = open(argv[1])
        src = load_src_from_maps(json.load(file))
        cfg = build_cfg(src)
        setup_contracts(cfg)
        sanitize_contracts(cfg)
        organize_calls(cfg)
        bind_register_to_value(cfg)

        rep_value = int(argv[3])
        heat = int(argv[4])

        for _ in range(0, rep_value):
            insert_garbage_instr(cfg)
        for _ in range(0, rep_value):
            imm_instr = get_immediate_instructions(cfg)
            if len(imm_instr) == 0:
                break
            curr_instr = imm_instr[randint(0, len(imm_instr) - 1)]
            obfuscate(cfg, curr_instr[0], curr_instr[1])
        for _ in range(0, rep_value):
            heatmap = register_heatmap(cfg, heat)
            substitute_reg(cfg, heatmap, heat)

        out = open(argv[5], "w+")
        out.write(str(src))


if __name__ == "__main__":
    main()
