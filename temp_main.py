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
import pandas as pd
from tqdm import tqdm
from time import time


def main():
    regenerate_graph = False
    
    budget = 8000
    threshold_factor=0.9
    threshold_iterations=10
    Cmax = 2
    random_parents=False
    score_beta = 0.5
    
    individuals_per_graph = 11
    generations=200
    
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
    
    computer_uses = [
        ComputerUses.DEFAULT,
        ComputerUses.GAMING,
        ComputerUses.STUDY,
        ComputerUses.VIDEO_EDITING,
    ]
    
    budgets = [
        2500,
        5000,
        10000,
        15000,
        30000,
    ]
    
    results = []
    
    for budget in budgets:
        for computer_use in computer_uses:
            components_priorities = get_normalized_priorities(computer_use)
    
            solution, score, price, history = tsbma_algorithm.calculate_best_solution(
                budget,
                generations=generations,
                individuals_per_graph=individuals_per_graph,
                threshold_iterations=threshold_iterations,
                components_priorities=components_priorities,
                random_parents=random_parents,
                score_beta=score_beta,
                use_prohibition_mecanism=True,
                max_components_to_swap=Cmax,
                threshold_factor=threshold_factor,
                initialization_threshold_factor=threshold_factor,
            )
            
            result = {
                "computer_use": computer_use.name,
                "budget": budget,
                "score": score,
                "price": price,
            }
            
            for tp, comp in solution.items():
                result[tp.name] = comp.name
                result[f"{tp.name}_score"] = comp.mark
                result[f"{tp.name}_pond_score"] = comp.mark * components_priorities[tp]
            
            results.append(result)

            df = pd.DataFrame(results)
            df.to_csv("generated_solutions.csv")
        exit()
        
    
    
    # paramters_to_test = {
    #     "score_beta": [0.2, 0.5, 0.8],
    #     "threshold_iterations": [3, 5, 10],
    #     "threshold_factor": [0, 1, 0.5, 0.9],
    #     "random_parents": [False, True],
    #     "max_components_to_swap": [1, 2, 3]
    # }
    
    # # Gera todas as combinações de parâmetros
    # keys, values = zip(*paramters_to_test.items())
    # combinations = [dict(zip(keys, v)) for v in product(*values)]

    # # Lista para armazenar os resultados
    # results = []

    # tsbma_algorithm = TSBMA(components, compatibility_subgraphs, cache_path=cache_path)

    # # Execute o algoritmo para cada combinação de parâmetros
    # for combination in tqdm(combinations):
    #     score_beta = combination["score_beta"]
    #     threshold_iterations = combination["threshold_iterations"]
    #     threshold_factor = combination["threshold_factor"]
    #     random_parents = combination["random_parents"]
    #     max_components_to_swap = combination["max_components_to_swap"]

        
    #     result, price = tsbma_algorithm.calculate_best_solution(
    #         budget,
    #         generations=generations,
    #         individuals_per_graph=individuals_per_graph,
    #         threshold_iterations=threshold_iterations,
    #         components_priorities=components_priorities,
    #         random_parents=random_parents,
    #         score_beta=score_beta,
    #         use_prohibition_mecanism=True,
    #         max_components_to_swap=max_components_to_swap,
    #         threshold_factor=threshold_factor,
    #     )
        
    #     # Adiciona os parâmetros e o resultado na lista
    #     results.append({
    #         "score_beta": score_beta,
    #         "threshold_factor": threshold_factor,
    #         "random_parents": random_parents,
    #         "threshold_iterations": threshold_iterations,
    #         "max_components_to_swap": max_components_to_swap,
    #         "result": result,
    #         "price": price,
    #     })
        
    #     df = pd.DataFrame(results)
    #     df.to_csv("results.csv")

if __name__ == "__main__":
    main()
