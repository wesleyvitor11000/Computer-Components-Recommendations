from components.Component import Component, ComponentTypes as ct
import operator as op
import networkx as nx
from matplotlib import pyplot as plt
from functools import partial
from tqdm import tqdm


def pci_in_pcis(data_lanes, sep, pci, pcis):
    if pci is None:
        return False

    for c_pcie in pcis:
        if data_lanes not in c_pcie:
            continue

        splited = c_pcie.split(sep)

        if len(splited) > 1 and splited[1][0] == "_":
            if pci == 1.0:
                return True

        try:
            version = float(splited[1][0])
            if pci == version:
                return True
        except:
            continue

    return False


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
    "pcie_in_x4_pcies": partial(pci_in_pcis, "x4", "pcie"),
    "pcie_in_x8_pcies": partial(pci_in_pcis, "x8", "pcie"),
    "pcie_in_x16_pcies": partial(pci_in_pcis, "x16", "pcie"),
    "is": lambda a, b: a == b,
    "is_not": lambda a, b: a != b,
}

constraint_one_var_operators = {
    "bool_vl": lambda a: a,
    "not": lambda a: not a,
    "gtz": lambda a: a > 0,
}

logical_operators = {
    "or": op.or_,
    "and": op.and_,
}


# lgc_gp: asign to a logical group
# lgc_op: logical operation with group
# apply for: wich component (0 or 1) will be considered in one var operator
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
        ],
        ct.GPU: [
            {
                "attr1": "is_empty",
                "op": "not",
                "apply_for": 1,
                "lgc_gp": 1,
                "lgc_op": "or",
            },
            {
                "attr1": "integrated_graphics",
                "op": "bool_vl",
                "apply_for": 0,
                "lgc_gp": 1,
                "lgc_op": "or",
            },
        ],
    },
    ct.SSD: {
        ct.MOTHERBOARD: [
            # verify if nvme is compatible
            {
                "attr1": "pcie",
                "attr2": "pci_slots",
                "op": "pcie_in_x4_pcies",
                "lgc_gp": 1,
                "lgc_op": "or",
            },
            {
                "attr1": "pcie",
                "attr2": "pci_slots",
                "op": "pcie_in_x8_pcies",
                "lgc_gp": 1,
                "lgc_op": "or",
            },
            {"attr1": "nvme", "op": "bool_vl", "lgc_gp": 1, "lgc_op": "and"},
            {"attr1": "nvme", "op": "not", "lgc_gp": 1, "lgc_op": "or"},
            # verify m2 compatibility
            {
                "attr1": "ssd_format",
                "op": "is",
                "arg": "M2",
                "apply_for": 0,
                "lgc_gp": 2,
                "lgc_op": "or",
            },
            {
                "attr1": "m2_sockets",
                "op": "gtz",
                "apply_for": 1,
                "lgc_gp": 2,
                "lgc_op": "and",
            },
            {
                "attr1": "ssd_format",
                "op": "is_not",
                "arg": "M2",
                "apply_for": 0,
                "lgc_gp": 2,
                "lgc_op": "or",
            },
            # verify sata3 compatibility
            {
                "attr1": "ssd_format",
                "op": "is",
                "arg": "2.5",
                "apply_for": 0,
                "lgc_gp": 3,
                "lgc_op": "or",
            },
            {
                "attr1": "sata3_connectors",
                "op": "gtz",
                "apply_for": 1,
                "lgc_gp": 3,
                "lgc_op": "and",
            },
            {
                "attr1": "ssd_format",
                "op": "is_not",
                "arg": "2.5",
                "apply_for": 0,
                "lgc_gp": 3,
                "lgc_op": "or",
            },
        ]
    },
    ct.GPU: {
        ct.MOTHERBOARD: [
            {
                "attr1": "is_empty",
                "op": "bool_vl",
                "apply_for": 0,
                "lgc_gp": 1,
                "lgc_op": "or",
            },
            {
                "attr1": "pcie",
                "attr2": "pci_slots",
                "op": "pcie_in_x16_pcies",
                "lgc_gp": 1,
                "lgc_op": "or",
            },
        ]
    },
    ct.RAM: {},
}


class CompatibilityGraphGenerator:
    def __init__(
        self, components: list[Component], constraints, intra_type_compatibility=False
    ):
        self.components = components
        self.constraints = constraints
        self.intra_type_compatibility = intra_type_compatibility

    def _verify_compability(self, comp1, comp2, constraints):
        compatible = True
        logicals = {}

        for constr in constraints:
            op_name = constr["op"]
            two_vars_op = op_name in constraint_two_var_operators
            op = (
                constraint_two_var_operators[op_name]
                if two_vars_op
                else constraint_one_var_operators[op_name]
            )

            apply_for = constr["apply_for"] if "apply_for" in constr else 0
            comp_to_apply = comp1 if apply_for == 0 else comp2
            attr1 = getattr(comp_to_apply, constr["attr1"])

            if two_vars_op:
                attr2 = (
                    getattr(comp2, constr["attr2"])
                    if "attr2" in constr
                    else constr["arg"]
                )

            if two_vars_op:
                compatible = op(attr1, attr2)
            else:
                compatible = op(attr1)

            if "lgc_gp" in constr:
                lgc_gp = constr["lgc_gp"]
                lgc_op = logical_operators[constr["lgc_op"]]
                logicals[lgc_gp] = (
                    lgc_op(logicals[lgc_gp], compatible)
                    if lgc_gp in logicals
                    else compatible
                )

            if not compatible and len(logicals) == 0:
                break

        if len(logicals) > 0:
            compatible = all(logicals.values())

        return compatible

    def _get_node_color(self, node_type):
        # Mapeia tipos de componente para cores
        color_map = {
            ct.CPU: "red",
            ct.MOTHERBOARD: "blue",
            ct.SSD: "green",
            ct.GPU: "gray",
            ct.RAM: "pink",
            # Adicione mais tipos e cores conforme necessário
        }
        return color_map.get(node_type, "lightblue")

    def generate_graph(self):
        G = nx.Graph()
        node_colors = {}

        for tp, comps in self.components.items():
            color = self._get_node_color(tp)
            for comp in comps:
                G.add_node(comp, subset=tp)
                node_colors[comp] = color

        i = 0

        for comp_type, comps_with_type in self.components.items():
            comp_type_constraints = compatibility_constraints[comp_type]
            print(f"generating for {comp_type.name}")
            for comp in tqdm(comps_with_type):
                for constr_comp_type in ct:
                    main_comp_checked = False
                    constrs = comp_type_constraints.get(constr_comp_type)

                    if (
                        constr_comp_type not in self.components
                        or constr_comp_type == comp_type
                        and not self.intra_type_compatibility
                    ):
                        continue

                    for constr_comp in self.components[constr_comp_type]:
                        i += 1
                        if comp == constr_comp:
                            main_comp_checked = True
                            continue

                        if constr_comp_type == comp_type and not main_comp_checked:
                            continue

                        if constr_comp_type in comp_type_constraints:
                            compatible = self._verify_compability(
                                comp, constr_comp, constrs
                            )
                        elif comp_type in compatibility_constraints[constr_comp_type]:
                            compatible = False
                            continue
                        else:
                            compatible = True

                        if compatible:
                            G.add_edge(comp, constr_comp)

        print(f"{i} iterations.")
        print(f"edges: {len(G.edges)}")

        # pos = nx.shell_layout(G)
        # labels = {node: node.name for node in G.nodes()}
        # nx.draw(G, pos, with_labels=False, labels=labels, node_color=[node_colors[node] for node in G.nodes()], font_weight='bold', font_size=8, node_size=100, alpha=0.9)
        # plt.show()

        return G
