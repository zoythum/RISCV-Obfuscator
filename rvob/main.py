import json
from sys import argv, exit
from rvob.rep.fragments import load_src_from_maps
from rvob.analysis.cfg import build_cfg
from rvob.setup_structures import setup_contracts, organize_calls, sanitize_contracts
from rvob.registerbinder import bind_register_to_value
from rvob.garbage_inserter import insert_garbage_instr
from rvob.obf.obfuscator import obfuscate
from rvob.scrambling import substitute_reg, NoSubstitutionException
from rvob.analysis.heatmaps import register_heatmap
from random import randint


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
            obfuscate(cfg)
        for _ in range(0, rep_value):
            heatmap = register_heatmap(cfg, heat)
            while True:
                try:
                    substitute_reg(cfg, heatmap, heat)
                    break
                except NoSubstitutionException:
                    pass

        out = open(argv[5], "w+")
        out.write(str(src))


if __name__ == "__main__":
    main()
