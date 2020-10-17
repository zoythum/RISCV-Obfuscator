import json
from typing import List, Tuple

import rvob.rep.base
import rvob.rep.fragments
import rvob.analysis
import rvob.registerbinder
import rvob.setup_structures
import rvob.assc_instr_block as assc_instr_block
import rvob.obf.obfuscator as obfuscator
import rvob.obf.const_derivation
import rvob.garbage_inserter as garbage_inserter
import rvob.analysis.heatmaps as heatmaps
import rvob.scrambling as scrambling
import rvob.analysis.tracer as tracer
from rvob.structures import Register
from rvob.registerbinder import ValueBlock
from rvob.obf.obfuscator import NotEnoughtRegisters, NotValidInstruction
from os import path

heat_map = None
heat_file = None
metrics_file = None
trace_heat_map = None
cfg = None


def write_heat( first: bool, frag: Tuple[int, int, int, int, int] = None):
    global trace_heat_map
    global heat_file
    global metrics_file

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
    if first:
        metrics_file.write("\nMean heat before: " + str(mean_heat)+"\n")
    else:
        metrics_file.write("\nMean heat after: " + str(mean_heat) + "\n")

    if frag is not None:
        metrics_file.write("Mean fragmentation: "+str(frag[0])+"\n")
        metrics_file.write("Fragmentation percentage: "+str((frag[1]/frag[2])*100)+"%\n")
        metrics_file.write("Mean variable life (frag accumulated): "+str(frag[3])+"\n")
        metrics_file.write("Mean variable life (frag separated): " + str(frag[4]) + "\n")


def calc_fragmentation():
    global cfg

    mean_frag_list: List[int] = []
    mean_life_scramb_list: List[int] = []
    mean_life_list: List[int] = []
    block_num: int = 0
    frag_block_num: int = 0

    for nd_id in cfg.nodes:
        frag_dict = {}
        life_dict = {}
        node = cfg.nodes[nd_id]
        if 'external' not in node:
            for v in node['reg_bind'].values():
                v: List[ValueBlock]
                block_num += len(v)
                for el in v:
                    mean_life_scramb_list.append(el.endline - el.initline + 1)
                    if not el.not_frag:
                        try:
                            frag_dict[el.group_id] += 1
                            life_dict[el.group_id] += (el.endline - el.initline + 1)
                        except KeyError:
                            frag_dict[el.group_id] = 1
                            life_dict[el.group_id] = (el.endline - el.initline + 1)
                    else:
                        mean_life_list.append((el.endline - el.initline + 1))
        for val in frag_dict.values():
            if val > 1:
                frag_block_num += val
                mean_frag_list.append(val)
        for val in life_dict.values():
            mean_life_list.append(val)

    mean_fragmentation: int = 0
    mean_life: int = 0
    mean_life_scramb: int = 0

    for elm in mean_frag_list:
        mean_fragmentation += elm
    mean_fragmentation //= len(mean_frag_list)

    for elm in mean_life_list:
        mean_life += elm
    mean_life //= len(mean_life_list)

    for elm in mean_life_scramb_list:
        mean_life_scramb += elm
    mean_life_scramb //= len(mean_life_scramb_list)

    return mean_fragmentation, frag_block_num, block_num, mean_life, mean_life_scramb



def do_scrambling():
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


def do_iter():
    global cfg
    global heat_map
    assc_instr_block.associate_instruction_to_ValueBlock(cfg)
    do_scrambling()
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

    do_scrambling()


def benchmark(name: str, entry: str):
    global heat_map
    global heat_file
    global metrics_file
    global trace_heat_map

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
    heat_map = heatmaps.register_heatmap(cfg, 50)
    dst = rel + '/benchmark/benchmark_output/' + name + ".txt"
    metric_dst = rel + '/benchmark/benchmark_output/' + name + "_metrics.txt"
    heat_file = open(dst, "w")
    metrics_file = open(metric_dst, "w")
    heat_file.write("Baseline:\n")
    trace_out = tracer.get_trace(cfg)
    trace_heat_map = trace_out[1]
    write_heat(first=True)
    heat_file.write("\n\n\nObuscated version:\n")
    do_iter()
    trace_out = tracer.get_trace(cfg, ex_path=trace_out[0])
    trace_heat_map = trace_out[1]
    write_heat(False, calc_fragmentation())
    heat_file.close()


def main():
    benchmarks = [('bubblesort', None), ('crc_32', None), ('dijkstra_small', None), ('fibonacci', None),
                  ('matrixMul', None), ('patricia', 'bit'), ('quickSort', None), ('sha', 'sha_transform')]
    for elem in benchmarks:
        print('\n\033[1mTesting ' + elem[0] + ':\033[0m')
        benchmark(elem[0], elem[1])


if __name__ == "__main__":
    main()
