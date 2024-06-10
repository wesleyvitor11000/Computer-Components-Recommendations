import networkx as nx
from components.Component import ComponentTypes as ct
import pickle
import os
from matplotlib import pyplot as plt

def get_node_color(node_type):
    # Mapeia tipos de componente para cores
    color_map = {
        ct.CPU: 'red',
        ct.MOTHERBOARD: 'blue',
        ct.SSD: 'green',
        ct.GPU: 'gray',
        ct.RAM: 'pink'
        # Adicione mais tipos e cores conforme necessário
    }
    return color_map.get(node_type, 'lightblue')

def find_valid_cliques_in_graph(graph, min_types_count=None):
    node_colors = {}
    if not min_types_count:
        min_types_count = len(ct)
    
    cliques = nx.clique.find_cliques(graph)
    valid_cliques = []
    c = 0
    print("filtering valid cliques...")
    for clq in cliques:
        c += 1
        print(f"verifying click {c} with len: {len(clq)}")
        
        H = nx.subgraph(graph, clq)
        
        for h in H:
            node_colors[h] = get_node_color(h.component_type)
        
        # fig, ax = plt.subplots()
        # nx.draw(H, ax=ax, node_color=[node_colors[node] for node in H.nodes()])
        
        # def on_key(event):
        #     if event.key == 'x':
        #         plt.close(fig)
        
        # fig.canvas.mpl_connect('key_press_event', on_key)
        
        # plt.show()
        
        
        types = set()
        for node in clq:
            if not node.component_type in types:
                types.add(node.component_type)
            if len(types) == min_types_count:
                break
        
        if len(types) != len(ct):
            continue
        
        valid_cliques.append(clq)
        
    print(f"{len(valid_cliques)} valid cliques from {c}")
    return valid_cliques


def save_cliques(cliques, save_path, file_name_pattern="clique_{}.pickle"):
    os.makedirs(save_path,exist_ok=True)
    file_path_pattern = f"{save_path}/{file_name_pattern}"
    
    for i, clq in enumerate(cliques):
        file_path = file_path_pattern.format(i)
        pickle.dump(clq, open(file_path, "wb"))
        
