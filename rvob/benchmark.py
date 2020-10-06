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
from rvob.structures import Register
from rvob.obf.obfuscator import NotEnoughtRegisters, NotValidInstruction
from os import path

heat_map = None
heat_file = None
trace_heat_map = None
cfg = None


def write_heat():
    global trace_heat_map
    global heat_file
    for i in range(len(trace_heat_map.keys())):
        heat_file.write(str(i) + ": " + str(trace_heat_map[i][0]) + " i:" + str(trace_heat_map[i][1].inserted) + " o_r: " + str(
            trace_heat_map[i][1].o_reg) + " n_r: " + str(trace_heat_map[i][1].n_reg) + " opcd: " + str(trace_heat_map[i][1].op_code) + "\n")
    mean_heat = [0]*len(Register)
    for val in trace_heat_map.values():
        for i in range(len(mean_heat)):
            mean_heat[i] += val[0][i]
    trace_length = len(trace_heat_map.keys())
    for i in range(len(mean_heat)):
        mean_heat[i] //= trace_length
    heat_file.write("\nMean heat: " + str(mean_heat)+"\n")



def do_iter():
    global cfg
    global heat_map

    for t in range(50):
        failed = 0
        print("scrambling iteration: " + str(t))
        heat_map = heatmaps.register_heatmap(cfg, 50)
        for z in range(50):
            try:
                scrambling.split_value_blocks(cfg, heat_map, 50)
                scrambling.substitute_reg(cfg, heat_map, 50)
                break
            except rvob.scrambling.NoSubstitutionException:
                if z == 50:
                    failed += 1
    print("Failure rate: " + str(failed/50 * 100) + "%")

    for t in range(5):
        failed = 0
        print("obfuscate iteration: " + str(t))
        for z in range(5):
            try:
                obfuscator.obfuscate(cfg)
                break
            except (NotEnoughtRegisters, NotValidInstruction):
                if z == 5:
                    failed += 1
    print("Failure rate: " + str(failed/5 * 100) + "%")

    for t in range(5):
        print("garbage iteration: " + str(t))
        garbage_inserter.insert_garbage_instr(cfg)

    for t in range(50):
        failed = 0
        print("scrambling iteration: " + str(t))
        heat_map = heatmaps.register_heatmap(cfg, 50)
        for z in range(50):
            try:
                scrambling.split_value_blocks(cfg, heat_map, 50)
                scrambling.substitute_reg(cfg, heat_map, 50)
                break
            except rvob.scrambling.NoSubstitutionException:
                if z == 50:
                    failed += 1
    print("Failure rate: " + str(failed / 50 * 100) + "%")


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
    global trace_heat_map
    trace_out = tracer.get_trace(cfg)
    trace_heat_map = trace_out[1]
    write_heat()
    heat_file.write("\n\n\nObuscated version:\n")
    do_iter()
    trace_out = tracer.get_trace(cfg, ex_path=trace_out[0])
    trace_heat_map = trace_out[1]
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
