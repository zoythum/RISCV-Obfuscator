from typing import List, Tuple, Mapping, MutableMapping

from networkx import DiGraph, all_simple_paths

from rep.base import to_line_iterator
from rep.fragments import CodeFragment
from structures import opcodes, Register


# TODO modify this function so that an external code node can be handled locally
def block_register_heat(block: CodeFragment,
                        max_heat: int,
                        init: List[int]) -> Tuple[Mapping[int, List[int]], List[int]]:
    """
    Calculate the register file's heatmap for the current block.

    :arg block: the block for which the heatmap has to be calculated
    :arg max_heat: the maximum heat level for a register
    :arg init: the initial register file's heat
    :return: a tuple containing the block's heatmap and the final heat of the register file
    """

    current_heat = list(init)
    heatmap = dict()
    for line in to_line_iterator(iter(block), block.begin):
        for r in range(0, len(current_heat)):
            # Don't let heat levels fall below 0
            if current_heat[r] > 0:
                current_heat[r] -= 1

        # Set the heat value to max_heat only if the rd register is being written
        if opcodes[line.statement.opcode][1]:
            current_heat[line.statement.r1.value] = max_heat

        heatmap[line.number] = list(current_heat)

    return heatmap, current_heat


def mediate_heat(heat_vector: List[List[int]]) -> List[int]:
    """
    Calculate the mean heat vector between the provided heat vectors.

    :arg heat_vector: a list of heat vectors of the same size
    :return: the mean heat vector
    """

    mean_vector = []
    vectors_num = len(heat_vector)

    # Assume that all heat vectors are of the same size
    for i in range(0, len(heat_vector[0])):
        sum_temp = 0
        for v in heat_vector:
            sum_temp += v[i]

        mean_vector.append(int(sum_temp / vectors_num))

    return mean_vector


def register_heatmap(cfg: DiGraph, max_heat: int) -> Mapping[int, List[int]]:
    """
    Calculate the register heatmap of the program.

    Given the program's representation as a CFG, an heatmap laid over all the reachable nodes is drawn.
    When a node on which multiple execution paths converge is found, its portion of heatmap is calculated starting from
    the mean heat levels of all the incoming arcs.
    :arg cfg: the program's representation as a CFG
    :arg max_heat: the maximum heat level a register can reach
    :return: an heatmap mapping every reachable line to a heat vector
    """

    # All nodes on which more than one execution flow converge
    merge_points = {node for node in cfg.nodes.keys() if cfg.in_degree(node) > 1 and node != 0}
    paths = list(all_simple_paths(cfg, 1, 0))
    # A collection of paths that cannot be completed because we still miss the initialization vector, indexed by node ID
    waiting_paths: MutableMapping[int, List[List[int]]] = {}
    # The scratchpad in which node heatmaps and final heat vectors are stored
    node_heatmaps: MutableMapping[int, Tuple[Mapping[int, List[int]], List[int]]] = {0: ({}, [0] * len(Register))}

    while len(paths) > 0:
        lin_path = paths.pop()

        # Don't recalculate heatmaps for already-visited nodes
        for node in filter(lambda n: n not in node_heatmaps, lin_path):
            if node in merge_points:
                if node not in waiting_paths:
                    # Multiple paths converge on this node and we miss the initialization vector: initialize the waiting
                    # paths list for this node and store the path's stump
                    del lin_path[:lin_path.index(node)]
                    waiting_paths[node] = [lin_path]
                    break
                elif frozenset(cfg.predecessors(node)).issubset(node_heatmaps):
                    # The initialization vector can finally be calculated: requeue all incomplete paths
                    paths.extend(waiting_paths[node])
                    del waiting_paths[node]
                    # Calculate this node's heatmap, mediating the incoming heat vectors
                    node_heatmaps[node] = block_register_heat(cfg.nodes[node]["block"],
                                                              max_heat,
                                                              mediate_heat([node_heatmaps[n][1] for n in
                                                                            cfg.predecessors(node)]))
                else:
                    # Multiple paths converge on this node and we miss the initialization vector: store the path's stump
                    del lin_path[:lin_path.index(node)]
                    waiting_paths[node].append(lin_path)
                    break
            else:
                # This node is part of a linear path: calculate its heatmap using the predecessor's final heat vector
                node_heatmaps[node] = block_register_heat(cfg.nodes[node]["block"],
                                                          max_heat,
                                                          node_heatmaps[next(cfg.predecessors(node))][1])

    heatmap = {}
    # Remove the initialization heat vector from the scratchpad
    del node_heatmaps[0]
    # Collapse the scratchpad into the resulting global heatmap
    for nhm in node_heatmaps.values():
        heatmap.update(nhm[0])

    return heatmap
