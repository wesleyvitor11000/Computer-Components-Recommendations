import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

<<<<<<< HEAD
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

=======
from graphs.CompatibilityGraph import CompatibilityGraph, compatibility_constraints
from components.Component import Component, ComponentTypes as ct
from components.components_loading import import_components
from random import Random


def main():
    
    components = import_components(files_variants={
        ct.MOTHERBOARD: "motherboards", ct.SSD: "ssds"
    })
    rd = Random()
    
    # rd.shuffle(components[ct.MOTHERBOARD])
    # rd.shuffle(components[ct.CPU])
    # rd.shuffle(components[ct.RAM])
    
    components[ct.MOTHERBOARD] = components[ct.MOTHERBOARD][:200:20]
    components[ct.SSD] = components[ct.SSD][:700:50]
    # components[ct.CPU] = components[ct.CPU][:200:20]
    # components[ct.RAM] = components[ct.RAM][:200:20]
    
    
    
    CompatibilityGraph(
        components,
        compatibility_constraints
    )


if __name__ == "__main__":
    main()
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
