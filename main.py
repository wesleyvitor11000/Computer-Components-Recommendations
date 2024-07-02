import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graphs.CompatibilityGraphGenerator import (
    CompatibilityGraphGenerator,
    compatibility_constraints,
)
from graphs import GraphsUtil
from components.Component import ComponentTypes as ct
from components.ComponentsLoading import import_components
from components import ComponentsUtil as comps_util
import pickle
from optimization_algorithms.TSBMA import TSBMA
from optimization_algorithms.computer_uses import (
    ComputerUses,
    get_normalized_priorities,
)
import shutil


def main():
    score_beta = 0.7
    budget = 5000
    regenerate_graph = False
    computer_use = ComputerUses.DEFAULT
    components_priorities = get_normalized_priorities(computer_use)
    
    graphs_path = "res/graphs/"
    cliques_path = f"{graphs_path}/cliques/"
    complete_graph_file = f"{graphs_path}/compatibility_complete_graph.pickle"
    graph_components_path = f"{graphs_path}/components.pickle"
    cache_path = f"{graphs_path}/cache/"

    if not os.path.exists(cliques_path) or regenerate_graph:
        components = import_components()

        components[ct.GPU].append(
            comps_util.create_fake_component(ct.GPU, name="empty_gpu", is_empty=True)
        )

        print("generating components groups...")
        components_groups = comps_util.group_components_attributes(
            components, comps_util.attributes_of_interest
        )
        groups_components = comps_util.convert_components_groups_to_components(
            components_groups
        )

        print("generating groups compatibility graph...")
        G = CompatibilityGraphGenerator(
            groups_components, compatibility_constraints, intra_type_compatibility=True
        ).generate_graph()

        print("finding cliques in groups compatibility graph...")
        groups_cliques = GraphsUtil.find_valid_cliques_in_graph(G)

        print("expanding cliques groups...")
        expanded_cliques = GraphsUtil.expand_cliques(groups_cliques, components_groups)

        if os.path.exists(graphs_path):
            shutil.rmtree(graphs_path)

        print("saving cliques components...")
        GraphsUtil.save_cliques(expanded_cliques, cliques_path)
        comps_util.save_components(components, graph_components_path)

    else:
        print("loading cliques components...")
        expanded_cliques = GraphsUtil.load_cliques(cliques_path)
        components = comps_util.load_components(graph_components_path)

    if not os.path.exists(complete_graph_file) or regenerate_graph:
        print("generating complete graph...")
        complete_graph = CompatibilityGraphGenerator(
            components, compatibility_constraints, intra_type_compatibility=False
        ).generate_graph()

        with open(complete_graph_file, "wb") as file:
            pickle.dump(complete_graph, file)
    else:
        print("loading complete compatibility graph...")
        with open(complete_graph_file, "rb") as file:
            complete_graph = pickle.load(file)

    print("getting compatibility subgraphs...")
    compatibility_subgraphs = GraphsUtil.get_subgraphs_from_cliques(
        expanded_cliques, complete_graph
    )

    tsbma_algorithm = TSBMA(components, compatibility_subgraphs, cache_path=cache_path)

    tsbma_algorithm.calculate_best_solution(
        budget,
        500,
        10,
        threshold_iterations=10,
        components_priorities=components_priorities,
        random_parents=True,
        score_beta=score_beta
    )


if __name__ == "__main__":
    main()
