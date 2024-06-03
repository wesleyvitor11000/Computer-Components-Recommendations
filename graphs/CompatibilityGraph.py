from components.Component import Component, ComponentTypes as ct
import operator as op
import networkx as nx
from matplotlib import pyplot as plt
from functools import partial

def pci_in_pcis(data_lanes, pcie, pcies, sep="pci"):
    print(pcie, pcies)
    
    if pcie is None:
        return False

    for c_pcie in pcies:
        splited = c_pcie.split(sep)

        if len(splited) > 1 and splited[1][0] == "_":
            if pcie == 1.0:
                return True
            
        if len(splited) > 1:
            print(splited[1][0])
            
        try:
            version = float(splited[1][0])
            if pcie == version:
                return True
        except:
            continue
            
    return False


pci_in_pcis("4", ["pcie4_x16_slots", 'pcie5_x16_slots', "pcie3_x16_slots", "pcie_x1_slots", "pci_l_slots", "pcie2_x16_slots", "pcie_x4_slots", "pcie_x8_slots"])

constraint_two_var_operators = {
    "eq": op.eq,
    "gt": op.gt,
    "lt": op.lt,
    "ge": op.ge,
    "le": op.le,
    "in": lambda a, b: a in b,
    "contains": lambda a, b: b in a,
    "gtz_bool": lambda a, b: a > 0 or not b,  # a greater than zero if b is true
    "bool_gtz": lambda a, b: not a or b > 0,  # b greater than zero if a is true
    "pcie_in_x4_pcies": partial(pci_in_pcis, "x4")
}

constraint_one_var_operators = {
    "bool_vl": lambda a: a,
    "not_bool": lambda a: not a
}

logical_operators = {
    "or": op.or_,
    "and": op.and_,
}


# lgc_gp: asign to a logical group
# lgc_op: logical operation with group
# operations are applied in sequential order
compatibility_constraints = {
    ct.MOTHERBOARD: {
        ct.CPU: [
            {"attr1": "socket", "attr2": "cpu_socket", "op": "eq"},
            {"attr1": "chipset", "attr2": "compatible_chipsets", "op": "in"},
        ],
        ct.RAM: [
            {"attr1": "ddr_version", "attr2": "ddr_version", "op": "eq"},
            {"attr1": "max_memory", "attr2": "total_ram_size", "op": "ge"},
            {"attr1": "ram_speed", "attr2": "memory_speed", "op": "ge"},
            {"attr1": "memory_slots", "attr2": "memory_modules", "op": "ge"},
        ],
    },
    ct.CPU: {
        ct.RAM: [
            {"attr1": "ddr_version", "attr2": "ddr_version", "op": "eq"},
            {"attr1": "max_mem_size", "attr2": "total_ram_size", "op": "ge"},
            {"attr1": "ram_speed_max", "attr2": "memory_speed", "op": "ge"},
        ]
    },
    ct.SSD: {
        ct.MOTHERBOARD: [
            {"attr1": "nvme", "op": "bool_vl", "lgc_gp": 1, "lgc_op": "or"},
            {"attr1": "pcie", "attr2": "pci_slots", "op": "pcie_in_pcies"},
        ]    
    },
    ct.RAM: {},
}


class CompatibilityGraph:
    def __init__(self, components: list[Component], constraints):
        self.vertices = components
        self.edges = self._generate_graph_edges(components, constraints)
        
    
    def _verify_compability(self, comp1, comp2, constraints):
        compatible = True
        logicals = {}
        
        for constr in constraints:
            op_name = constr["op"]
            two_vars_op = op_name in constraint_two_var_operators
            op = constraint_two_var_operators[op_name] if two_vars_op\
                else constraint_one_var_operators[op_name]
            
            attr1 = getattr(comp1, constr["attr1"]) 
            if two_vars_op:
                attr2 = getattr(comp2, constr["attr2"])
            
            if two_vars_op:
                compatible = op(attr1, attr2)
            else:
                compatible = op(attr1)
            
            if not compatible:
                break
            
        return compatible
        
    

    def _generate_graph_edges(self, components: dict[ct, list], constraints):
        G = nx.Graph()
        
        for tp, comps in components.items():
            for comp in comps:
                G.add_node(f"{comp.name}", subset=tp)

        # TODO: separar o loop com uma função de verificar compatibilidade
        # TODO: corrigir lógica de compatibilidade comp1 compativel com comp2, mas comp2 incompativel com comp1
        i = 0

        for comp_type, comps_with_type in components.items():
            comp_type_constraints = compatibility_constraints[comp_type]
            
            for comp in comps_with_type:
                for constr_comp_type in ct:
        
                    constrs = comp_type_constraints.get(constr_comp_type)
                    
                    if constr_comp_type not in components or constr_comp_type == comp_type:
                        continue
                    
                    for constr_comp in components[constr_comp_type]:
                        i += 1
                        # print(comp, constr_comp_type, constrs, constr_comp, sep="\n")
                        if constr_comp_type in comp_type_constraints:
                            compatible = self._verify_compability(comp, constr_comp, constrs)
                        elif comp_type in compatibility_constraints[constr_comp_type]:
                            compatible = False
                            continue
                        else:
                            compatible = True
                        
                        if compatible:
                            G.add_edge(comp.name, constr_comp.name)
        print(i)
        pos = nx.multipartite_layout(G)
        labels = nx.get_node_attributes(G, 'subset')
        
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', font_size=8)
        nx.draw_networkx_labels(G, pos, labels=labels)
        plt.show()
                            
                        

