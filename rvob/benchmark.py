import json
import rvob.rep.base
import rvob.rep.fragments
import rvob.analysis
import rvob.registerbinder
import rvob.setup_structures
import rvob.obf.obfuscator as obfuscator
import rvob.obf.const_derivation
import rvob.garbage_inserter as garbage_inserter
import rvob.analysis.heatmaps as heatmaps
import rvob.scrambling as scrambling
import rvob.analysis.tracer as tracer
from os import path

heat_map = None
heat_file = None
out = None
cfg = None


def write_heat():
    global out
    for i in range(len(out[1].keys())):
        global heat_file
        heat_file.write(str(i) + ": " + str(out[1][i][0]) + " i:" + str(out[1][i][1].inserted) + " o_r: " + str(
            out[1][i][1].o_reg) + " n_r: " + str(out[1][i][1].n_reg) + " opcd: " + str(out[1][i][1].op_code) + "\n")


def do_iter():
    global cfg
    global heat_map

    for t in range(50):
        print("scrambling iteration: " + str(t))
        heat_map = heatmaps.register_heatmap(cfg, 50)
        for _ in range(50):
            try:
                scrambling.split_value_blocks(cfg, heat_map, 50)
                scrambling.substitute_reg(cfg, heat_map, 50)
                break
            except rvob.scrambling.NoSubstitutionException:
                pass

    for t in range(5):
        print("obfuscate iteration: " + str(t))
        obfuscator.obfuscate(cfg)

    for t in range(5):
        print("garbage iteration: " + str(t))
        garbage_inserter.insert_garbage_instr(cfg)

    for t in range(50):
        print("scrambling iteration: " + str(t))
        heat_map = heatmaps.register_heatmap(cfg, 50)
        for _ in range(50):
            try:
                scrambling.split_value_blocks(cfg, heat_map, 50)
                scrambling.substitute_reg(cfg, heat_map, 50)
                break
            except rvob.scrambling.NoSubstitutionException:
                pass


def benchmark(name: str, entry: str):
    rel = path.dirname(__file__)
    src = rel + '/benchmark/benchmark_file/' + name + '.json'
    file = open(src)
    src = rvob.rep.fragments.load_src_from_maps(json.load(file))
    global cfg
    if entry is None:
        cfg = rvob.analysis.cfg.build_cfg(src)
    else:
        cfg = rvob.analysis.cfg.build_cfg(src, entry)
    rvob.setup_structures.setup_contracts(cfg)
    rvob.setup_structures.sanitize_contracts(cfg)
    rvob.setup_structures.organize_calls(cfg)
    rvob.registerbinder.bind_register_to_value(cfg)
    global heat_map
    heat_map = heatmaps.register_heatmap(cfg, 50)
    dst = rel + '/benchmark/benchmark_output/' + name + ".txt"
    global heat_file
    heat_file = open(dst, "w")
    heat_file.write("Baseline:\n")
    global out
    out = tracer.get_trace(cfg)
    write_heat()
    heat_file.write("\n\n\nObuscated version:\n")
    do_iter()
    out = tracer.get_trace(cfg, ex_path=out[0])
    write_heat()
    heat_file.close()


def main():
    benchmarks = [('bubblesort', None), ('crc_32', None), ('dijkstra_small', None), ('fibonacci', None),
                  ('matrixMul', None), ('patricia', 'bit'), ('quickSort', None), ('sha', 'sha_transform')]
    for elem in benchmarks:
        print('\n\033[1mTesting ' + elem[0] + ':\033[0m')
        benchmark(elem[0], elem[1])


if __name__ == "__main__":
    main()
