import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graphs.CompatibilityGraphGenerator import CompatibilityGraphGenerator, compatibility_constraints
from graphs import GraphsUtil
from components.Component import Component, GPU, ComponentTypes as ct
from components.components_loading import import_components
from components import ComponentsUtil
import networkx as nx
from matplotlib import pyplot as plt
import pickle
from pprint import pprint


def main():

    regenerate_graph = True

    components = import_components(
        files_variants={ct.MOTHERBOARD: "motherboards", ct.RAM: "memories", ct.SSD: "ssds", ct.CPU: "cpus", ct.GPU: "gpus"}
    )
    

    components[ct.GPU].append(
        ComponentsUtil.create_fake_component(ct.GPU, name="empty_gpu", is_empty=True)
    )
    
    components_groups = ComponentsUtil.group_components_attributes(components, ComponentsUtil.attributes_of_interest)    
    groups_components = ComponentsUtil.convert_components_groups_to_components(components_groups)

    
    graph_generator = CompatibilityGraphGenerator(groups_components, compatibility_constraints, intra_type_compatibility=True)
    G = graph_generator.generate_graph()
    print("saving compatibility graph...")
        
    
    print(f"normal: {len(G.edges)}")    
    cliques = GraphsUtil.find_valid_cliques_in_graph(G)

if __name__ == "__main__":
    main()

