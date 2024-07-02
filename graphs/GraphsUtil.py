import networkx as nx
from components.Component import ComponentTypes as ct
from components import ComponentsUtil
import pickle
import os
from matplotlib import pyplot as plt
from tqdm import tqdm
import yaml


def get_separated_components_from_graph(graph):
    components = {tp: [] for tp in ct}
    [components[node.component_type].append(node) for node in graph.nodes]

    for tp in components.keys():
        components[tp] = sorted(components[tp], key=lambda c: c.price)

    return components


def is_clique(graph):
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    max_edges = num_nodes * (num_nodes - 1) // 2
    return num_edges == max_edges


def get_node_color(node_type):
    color_map = {
        ct.CPU: "red",
        ct.MOTHERBOARD: "blue",
        ct.SSD: "green",
        ct.GPU: "gray",
        ct.RAM: "pink",
    }
    return color_map.get(node_type, "lightblue")


def expand_clique(clique, components_groups, attributes_names=None):
    expanded_clique = []
    for node in clique:
        node_group_key = ComponentsUtil.get_component_group_key(node, attributes_names)
        expanded_clique.extend(components_groups[node.component_type][node_group_key])

    return expanded_clique


def expand_cliques(cliques, components_groups, attributes_names=None):
    expanded_cliques = []
    for clique in tqdm(cliques):
        expanded_clique = expand_clique(clique, components_groups, attributes_names)
        expanded_cliques.append(expanded_clique)

    return expanded_cliques


def find_valid_cliques_in_graph(graph, min_types_count=None):
    node_colors = {}
    if not min_types_count:
        min_types_count = len(ct)

    cliques = nx.clique.find_cliques(graph)
    valid_cliques = set()
    c = 0
    print("filtering valid cliques...")
    clq1 = None
    for clq in cliques:
        c += 1

        print(f"verifying click {c} with len: {len(clq)}")

        H = nx.subgraph(graph, clq)

        for h in H:
            node_colors[h] = get_node_color(h.component_type)

        types = set()
        for node in clq:
            if not node.component_type in types:
                types.add(node.component_type)
            if len(types) == min_types_count:
                break

        if len(types) != len(ct):
            continue

        if not clq1:
            clq1 = clq

        valid_cliques.add(tuple(sorted(clq, key=lambda x: x.name)))

    print(f"{len(valid_cliques)} valid cliques from {c}")
    return valid_cliques


def get_subgraphs_from_cliques(cliques, complete_graph):
    subgraphs = []
    for clique in tqdm(cliques):
        subgraph = nx.subgraph(complete_graph, clique)
        subgraphs.append(subgraph)

    return subgraphs


def save_cliques(cliques, save_path, file_name_pattern="clique_{}.pickle"):
    os.makedirs(save_path, exist_ok=True)
    file_path_pattern = f"{save_path}/{file_name_pattern}"

    for i, clq in enumerate(cliques):
        file_path = file_path_pattern.format(i)
        with open(file_path, "wb") as file:
            pickle.dump(clq, file)


def load_cliques(cliques_path, file_name_pattern="clique_{}.pickle"):
    cliques = []
    file_path_pattern = f"{cliques_path}/{file_name_pattern}"
    i = 0
    while True:
        clique_path = file_path_pattern.format(i)

        if os.path.exists(clique_path):
            with open(clique_path, "rb") as file:
                clique = pickle.load(file)
                cliques.append(clique)
        else:
            break

        i += 1

    return cliques
