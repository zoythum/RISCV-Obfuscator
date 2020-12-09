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
mean_unp_life: int = 0


def write_heat( first: bool, frag: Tuple[int, List[int], int, int, int] = None):
    global trace_heat_map
    global heat_file
    global metrics_file
    global mean_unp_life

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
        metrics_file.write("Mean heat before: " + str(mean_heat)+"\n")
    else:
        metrics_file.write("Mean heat after: " + str(mean_heat) + "\n")

    if frag is not None:
        # The frag tuple contains the following value:
        # [0] mean fragmentation
        # [1] list of the fragmented ValueBlock with fragment number for each ValueBlock
        # [2] number of original ValueBlock
        # [3] mean life (aggregated fragments)
        # [4] mean life scrambled (single fragment)
        metrics_file.write("Mean fragmentation: "+str(frag[0])+"\n")
        metrics_file.write("Mean variable life (unprotected case): " + str(mean_unp_life) + "\n")
        metrics_file.write("Mean variable life (frag accumulated): "+str(frag[3])+"\n")
        metrics_file.write("Mean variable life (frag separated): " + str(frag[4]) + "\n")
        metrics_file.write("Number of original ValueBlock: " + str(frag[2]) + "\n")
        metrics_file.write("List of fragmented ValueBlock: " + str(frag[1]) + "-> " + str(len(frag[1])) + "\n")



def calc_fragmentation():
    global cfg

    mean_frag_list: List[int] = []
    mean_life_scramb_list: List[int] = []
    mean_life_list: List[int] = []
    block_num: int = 0

    for nd_id in cfg.nodes:
        frag_dict: Dict[int, Set[Register]] = {}
        life_dict = {}
        node = cfg.nodes[nd_id]
        if 'external' not in node:
            for it in node['reg_bind'].items():
                k: Register = it[0]
                v: List[ValueBlock] = it[1]
                v = [blk for blk in v if not blk.inserted]  # eliminate block added by some garbage instruction
                for el in v:
                    mean_life_scramb_list.append(el.end_line - el.init_line + 1)
                    # this check exclude the block that have the same group_id only because all of them start from the
                    # first line of the node, but they aren't part of the same original ValueBlock
                    if el.group_id is not None:
                        try:
                            frag_dict[el.group_id].add(k)
                            life_dict[el.group_id] += (el.end_line - el.init_line + 1)
                        except KeyError:
                            frag_dict[el.group_id] = {k}
                            life_dict[el.group_id] = (el.end_line - el.init_line + 1)
                            block_num += 1
                    else:
                        block_num += 1
                        mean_frag_list.append(1)
                        mean_life_list.append((el.end_line - el.init_line + 1))
        for val in frag_dict.values():
            mean_frag_list.append(len(val))
        for val in life_dict.values():
            mean_life_list.append(val)

    mean_fragmentation: int = 0
    mean_life: int = 0
    mean_life_scramb: int = 0

    src_list = []
    for elm in mean_frag_list:
        mean_fragmentation += elm
        if elm > 1:
            src_list.append(elm)
    mean_fragmentation //= len(mean_frag_list)

    for elm in mean_life_list:
        mean_life += elm
    mean_life //= len(mean_life_list)

    for elm in mean_life_scramb_list:
        mean_life_scramb += elm
    mean_life_scramb //= len(mean_life_scramb_list)

    return mean_fragmentation, src_list, block_num, mean_life, mean_life_scramb


def calc_var_life():
    global cfg
    global mean_unp_life

    life_list: List[int] = []
    for n in cfg.nodes:
        if 'external' not in cfg.nodes[n]:
            reg_bind: Dict[Register, List[ValueBlock]] = cfg.nodes[n]['reg_bind']
            for val in reg_bind.values():
                for elm in val:
                    life_list.append(elm.end_line - elm.init_line + 1)

    mean_life: int = 0
    for elm in life_list:
        mean_life += elm

    mean_unp_life = mean_life // len(life_list)


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

    print("Splitting failure rate: " + str(failed_splitting/iter_num * 100) + "%")
    print("Substitution failure rate: " + str(failed_substitute / iter_num * 100) + "%")


def do_iter():
    global cfg
    global heat_map
    do_scrambling(1000)
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

    do_scrambling(1000)


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
    calc_var_life()
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
