from abc import abstractmethod, ABC
from graphs import GraphsUtil
from tqdm import tqdm


class OptimizationAlgorithm(ABC):
    def __init__(self, compatibility_graphs) -> None:
        self.compatibility_graphs = compatibility_graphs
        self.graphs_components = self.separate_graphs_components(compatibility_graphs)
        self.components_graphs = self.get_graphs_from_components(compatibility_graphs)

    def separate_graphs_components(self, graphs):
        graphs_separated_components = {}

        for graph in tqdm(graphs):
            graphs_separated_components[graph] = (
                GraphsUtil.get_separated_components_from_graph(graph)
            )

        return graphs_separated_components

    def get_graphs_from_components(self, graphs):
        components_graphs = {}

        for graph in graphs:
            for component in graph.nodes:
                if component not in components_graphs:
                    components_graphs[component] = {graph}
                else:
                    components_graphs[component].add(graph)

        return components_graphs

    def filter_graphs_with_all_component(self, components):
        graphs_with_components = [self.components_graphs[comp] for comp in components]
        return graphs_with_components

    @abstractmethod
    def calculate_best_solution(self, budget):
        pass
