import os
import sys
import json

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
from time import time


def main():
    regenerate_graph = False
    
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
        
        print(f"groups graph size: nodes = {len(G.nodes)}, edges: {len(G.edges)}")

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
        print("loading components cliques...")
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
    
    print("initializing TSBMA")
    tsbma_algorithm = TSBMA(components, compatibility_subgraphs, cache_path=cache_path)
    
    computer_uses_names = {use.name: use for use in ComputerUses}
    
    while True:
        config_path = input("Digite o caminho para o arquivo de configuração, ou 0 para sair:\n")
        
        if config_path == "0":
            break
        
        with open(config_path, "r") as file:
            configs = json.load(file)
        
        computer_use = ComputerUses(
            computer_uses_names[configs["computer_use"]]
        )
        components_priorities = get_normalized_priorities(computer_use)
        
        budget = float(configs["budget"])
        individuals_per_graph = int(configs["individuals_per_graph"])
        generations = int(configs["generations"])
        threshold_iterations = int(configs["threshold_iterations"])
        random_selection = bool(configs["random_selection"])
        beta=float(configs["beta"])
        max_components_to_swap=int(configs["cmax"])
        threshold_factor=float(configs["threshold_a"])
        
        start = time()
        solution, score, price, history = tsbma_algorithm.calculate_best_solution(
            budget,
            generations=generations,
            individuals_per_graph=individuals_per_graph,
            threshold_iterations=threshold_iterations,
            components_priorities=components_priorities,
            random_parents= random_selection,
            score_beta=beta,
            use_prohibition_mecanism=True,
            max_components_to_swap=max_components_to_swap,
            threshold_factor=threshold_factor,
        )
        end = time()
        
        print("\nSolution:")
        solution_string = [print(f"{c[0].name}: {c[1].name} (score: {c[1].mark/5}, price: R$ {c[1].price}).") for c in solution.items()]
        print(solution_string)
        
        print(f"\nPontuação: {score}.")
        print(f"Preço: R$ {price}.")
        print(f"Gerada em {end-start} segundos.\n")
        
    
if __name__ == "__main__":
    main()