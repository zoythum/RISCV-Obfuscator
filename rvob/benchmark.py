import json
from typing import List, Tuple, Dict, Set

from networkx import DiGraph

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
from rvob.registerbinder import ValueBlock
from rvob.obf.obfuscator import NotEnoughtRegisters, NotValidInstruction
from os import path

heat_map = None
heat_file = None
metrics_file = None
trace_heat_map = None
cfg: DiGraph = None


def write_heat(first: bool, frag: Tuple[int, List[int], int, int, int] = None):
    global trace_heat_map
    global heat_file
    global metrics_file

    for i in range(len(trace_heat_map.keys())):
        heat_file.write(
            str(i) + ": " + str(trace_heat_map[i][0]) + " i:" + str(trace_heat_map[i][1].inserted) + " o_r: " + str(
                trace_heat_map[i][1].o_reg) + " n_r: " + str(trace_heat_map[i][1].n_reg) + " opcd: " + str(
                trace_heat_map[i][1].op_code) + "\n")
    mean_heat = [0] * len(Register)
    for val in trace_heat_map.values():
        for i in range(len(mean_heat)):
            mean_heat[i] += val[0][i]
    trace_length = len(trace_heat_map.keys())
    for i in range(len(mean_heat)):
        mean_heat[i] //= trace_length
    if first:
        metrics_file.write("Mean heat before: " + str(mean_heat) + "\n")
    else:
        metrics_file.write("Mean heat after: " + str(mean_heat) + "\n")

    if frag is not None:
        # The frag tuple contains the following value:
        # [0] mean fragmentation
        # [1] list of the fragmented ValueBlock with fragment number for each ValueBlock
        # [2] number of original ValueBlock
        metrics_file.write("Mean fragmentation: " + str(frag[0]) + "\n")
        metrics_file.write("Number of original ValueBlock: " + str(frag[2]) + "\n")
        metrics_file.write("List of fragmented ValueBlock: " + str(frag[1]) + "-> " + str(len(frag[1])) + "\n")


def analyze_node(node: DiGraph.node, frag_dict: Dict[int, Set[Register]], frag_list: List[int]) -> int:
    block_num: int = 0
    for (reg, v) in node['reg_bind'].items():
        v = [blk for blk in v if not blk.inserted]  # eliminate block added by some garbage instruction
        for block in v:
            # this check exclude the block that have the same group_id only because all of them start from the
            # first line of the node, but they aren't part of the same original ValueBlock
            if block.group_id is not None:
                try:
                    frag_dict[block.group_id].add(reg)
                except KeyError:
                    frag_dict[block.group_id] = {reg}
                    block_num += 1
            else:
                block_num += 1
                frag_list.append(1)
    return block_num


def calc_fragmentation():
    global cfg

    frag_list: List[int] = []  # indicates how many fragments have each block of the program
    block_num: int = 0

    for nd_id in cfg.nodes:
        node = cfg.nodes[nd_id]
        frag_dict: Dict[int, Set[Register]] = {}
        if 'external' not in node:
            block_num += analyze_node(node, frag_dict, frag_list)
            for val in frag_dict.values():
                frag_list.append(len(val))

    src_list = [elm for elm in frag_list if elm > 1]
    mean_fragmentation = sum(frag_list)
    mean_fragmentation //= len(frag_list)

    return mean_fragmentation, src_list, block_num


def do_scrambling(iter_num: int):
    global cfg
    global heat_map
    failed_splitting = 0
    failed_substitute = 0

    for t in range(iter_num):
        print("scrambling iteration: " + str(t))
        heat_map = heatmaps.register_heatmap(cfg, 50)

        # try to do a register substitution
        ret = scrambling.split_value_blocks(cfg, heat_map, 50)
        if ret == -1:
            failed_splitting += 1

        # try to substitute the usage of a register
        ret = scrambling.substitute_reg(cfg, heat_map, 50)
        if ret == -1:
            failed_substitute += 1

    print("Splitting failure rate: " + str(failed_splitting / iter_num * 100) + "%")
    print("Substitution failure rate: " + str(failed_substitute / iter_num * 100) + "%")


def do_iter():
    global cfg
    global heat_map
    do_scrambling(5)
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
    print("Failure rate: " + str(failed / 5 * 100) + "%")

    for t in range(5):
        print("garbage iteration: " + str(t))
        garbage_inserter.insert_garbage_instr(cfg)

    # do_scrambling(1000)


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
    sub_test = [('bubblesort', None)]
    for elem in sub_test:
        print('\n\033[1mTesting ' + elem[0] + ':\033[0m')
        benchmark(elem[0], elem[1])


if __name__ == "__main__":
    main()
