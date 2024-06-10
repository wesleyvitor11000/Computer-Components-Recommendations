import networkx as nx
import matplotlib.pyplot as plt

# Definição das regras de compatibilidade
compatibility_rules = [
    {
        "component_type_1": "motherboard",
        "attribute_1": "socket",
        "component_type_2": "cpu",
        "attribute_2": "cpu_socket",
        "logical_operator": "==",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "motherboard",
        "attribute_1": "chipset",
        "component_type_2": "cpu",
        "attribute_2": "compatible_chipsets",
        "logical_operator": "in",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "motherboard",
        "attribute_1": "max_memory",
        "component_type_2": "memory",
        "attribute_2": "total_ram_size",
        "logical_operator": ">=",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "motherboard",
        "attribute_1": "ddr_version",
        "component_type_2": "memory",
        "attribute_2": "ddr_version",
        "logical_operator": "==",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "motherboard",
        "attribute_1": "ram_speed",
        "component_type_2": "memory",
        "attribute_2": "memory_speed",
        "logical_operator": ">=",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "motherboard",
        "attribute_1": "pcie_x16_slots",
        "component_type_2": "graphics-card",
        "attribute_2": "pcie",
        "logical_operator": "contains",
        "comparison_type_1": "slot_version",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "cpu",
        "attribute_1": "ram_speed_max",
        "component_type_2": "memory",
        "attribute_2": "memory_speed",
        "logical_operator": ">=",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "cpu",
        "attribute_1": "ddr_version",
        "component_type_2": "memory",
        "attribute_2": "ddr_version",
        "logical_operator": "==",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "cpu",
        "attribute_1": "mem_channels",
        "component_type_2": "motherboard",
        "attribute_2": "memory_channels",
        "logical_operator": "==",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "value",
=======
        "comparison_type_2": "value"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "ssd",
        "attribute_1": "nvme",
        "component_type_2": "motherboard",
        "attribute_2": "m2_sockets",
        "logical_operator": ">=",
        "comparison_type_1": "count",
<<<<<<< HEAD
        "comparison_type_2": "count",
=======
        "comparison_type_2": "count"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "ssd",
        "attribute_1": "pcie",
        "component_type_2": "motherboard",
        "attribute_2": "pcie_x4_slots",
        "logical_operator": ">=",
        "comparison_type_1": "count",
<<<<<<< HEAD
        "comparison_type_2": "count",
=======
        "comparison_type_2": "count"
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    },
    {
        "component_type_1": "graphics-card",
        "attribute_1": "pcie",
        "component_type_2": "motherboard",
        "attribute_2": "pcie_x16_slots",
        "logical_operator": "contains",
        "comparison_type_1": "value",
<<<<<<< HEAD
        "comparison_type_2": "slot_version",
    },
]


=======
        "comparison_type_2": "slot_version"
    }
]

>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
# Função para verificar compatibilidade
def is_compatible(comp1, comp2, rule):
    attr1 = comp1.get(rule["attribute_1"])
    attr2 = comp2.get(rule["attribute_2"])
<<<<<<< HEAD

=======
    
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    if rule["comparison_type_1"] == "count":
        attr1 = len(attr1) if isinstance(attr1, list) else 0
    if rule["comparison_type_2"] == "count":
        attr2 = len(attr2) if isinstance(attr2, list) else 0
<<<<<<< HEAD

=======
        
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    if rule["logical_operator"] == "==":
        return attr1 == attr2
    elif rule["logical_operator"] == ">=":
        return attr1 >= attr2
    elif rule["logical_operator"] == "in":
        # Verificar se ambos são iteráveis (listas) antes de verificar a inclusão
<<<<<<< HEAD
        return (
            isinstance(attr1, list)
            and isinstance(attr2, list)
            and all(elem in attr1 for elem in attr2)
        )
    elif rule["logical_operator"] == "contains":
        # Verificar se ambos são iteráveis (listas) antes de verificar a inclusão
        return (
            isinstance(attr1, list)
            and isinstance(attr2, list)
            and all(elem in attr2 for elem in attr1)
        )
=======
        return isinstance(attr1, list) and isinstance(attr2, list) and all(elem in attr1 for elem in attr2)
    elif rule["logical_operator"] == "contains":
        # Verificar se ambos são iteráveis (listas) antes de verificar a inclusão
        return isinstance(attr1, list) and isinstance(attr2, list) and all(elem in attr2 for elem in attr1)
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    else:
        return False


<<<<<<< HEAD
# Função para criar o grafo de compatibilidade
def create_compatibility_graph(components):
    G = nx.Graph()

    # Adicionando nós
    for component in components:
        G.add_node(component["name"], type=component["type"])

=======

# Função para criar o grafo de compatibilidade
def create_compatibility_graph(components):
    G = nx.Graph()
    
    # Adicionando nós
    for component in components:
        G.add_node(component["name"], type=component["type"])
    
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    # Verificando compatibilidade e adicionando arestas
    for rule in compatibility_rules:
        for comp1 in components:
            for comp2 in components:
<<<<<<< HEAD
                if (
                    comp1["type"] == rule["component_type_1"]
                    and comp2["type"] == rule["component_type_2"]
                ):
                    if is_compatible(comp1, comp2, rule):
                        G.add_edge(comp1["name"], comp2["name"])

    return G


# Função para plotar o grafo de compatibilidade
def plot_compatibility_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "type")

    nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold")
    nx.draw_networkx_labels(G, pos, labels=labels)
    plt.show()


# Exemplo de uso
components = [
    {
        "name": "Motherboard1",
        "type": "motherboard",
        "socket": "AM4",
        "chipset": "B450",
        "max_memory": 64,
        "ddr_version": 4,
        "ram_speed": 3200,
        "pcie_x16_slots": [3],
        "memory_channels": 2,
        "m2_sockets": 2,
        "pcie_x4_slots": 2,
    },
    {
        "name": "CPU1",
        "type": "cpu",
        "cpu_socket": "AM4",
        "compatible_chipsets": ["B450", "X470"],
        "ram_speed_max": 3200,
        "ddr_version": 4,
        "mem_channels": 2,
    },
    {
        "name": "Memory1",
        "type": "memory",
        "memory_speed": 3200,
        "ddr_version": 4,
        "total_ram_size": 16,
    },
    {"name": "SSD1", "type": "ssd", "nvme": 1, "pcie": 3},
    {"name": "GPU1", "type": "graphics-card", "pcie": 3},
=======
                if comp1["type"] == rule["component_type_1"] and comp2["type"] == rule["component_type_2"]:
                    if is_compatible(comp1, comp2, rule):
                        G.add_edge(comp1["name"], comp2["name"])
    
    return G

# Função para plotar o grafo de compatibilidade
def plot_compatibility_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'type')
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels=labels)
    plt.show()

# Exemplo de uso
components = [
    {"name": "Motherboard1", "type": "motherboard", "socket": "AM4", "chipset": "B450", "max_memory": 64, "ddr_version": 4, "ram_speed": 3200, "pcie_x16_slots": [3], "memory_channels": 2, "m2_sockets": 2, "pcie_x4_slots": 2},
    {"name": "CPU1", "type": "cpu", "cpu_socket": "AM4", "compatible_chipsets": ["B450", "X470"], "ram_speed_max": 3200, "ddr_version": 4, "mem_channels": 2},
    {"name": "Memory1", "type": "memory", "memory_speed": 3200, "ddr_version": 4, "total_ram_size": 16},
    {"name": "SSD1", "type": "ssd", "nvme": 1, "pcie": 3},
    {"name": "GPU1", "type": "graphics-card", "pcie": 3}
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
]

G = create_compatibility_graph(components)
plot_compatibility_graph(G)
