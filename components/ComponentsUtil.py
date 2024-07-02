from .Component import ComponentTypes as ct, type_to_comp_class_map, Component
from pprint import pprint
import os
import pickle
from tqdm import tqdm

attributes_of_interest = {
    ct.MOTHERBOARD: [
        "socket",
        "chipset",
        "ddr_version",
        "max_memory",
        "ram_speed",
        "memory_slots",
        "pci_slots",
        "m2_sockets",
        "sata3_connectors",
    ],
    ct.RAM: ["ddr_version", "total_ram_size", "memory_speed", "memory_modules"],
    ct.SSD: ["pcie", "nvme", "ssd_format"],
    ct.CPU: [
        "cpu_socket",
        "compatible_chipsets",
        "ddr_version",
        "max_mem_size",
        "ram_speed_max",
        "integrated_graphics",
    ],
    ct.GPU: ["is_empty", "pcie"],
}


def create_fake_component(component_type: ct, **kwargs) -> Component:
    comp_class = type_to_comp_class_map[component_type]

    atributes = {
        attr: tp()
        for attr, tp in {
            **Component.__annotations__,
            **comp_class.__annotations__,
        }.items()
        if attr != "uid"
    }
    atributes.update(kwargs)

    return comp_class(**atributes)


def get_components_hamming_distances(components, cache_path=None):
    cache_file = ""

    if cache_path:
        cache_file = f"{cache_path}/components_distances.pickle"

        if os.path.exists(cache_file):
            print("loading hamming distances...")
            with open(cache_file, "rb") as file:
                components_distances = pickle.load(file)

            return components_distances

    os.makedirs(cache_path, exist_ok=True)
    components_distances = {}

    print("calculating components distances...")
    for tp in tqdm(ct):
        attrs = get_attributes_names_from_component_type(tp)

        for comp1 in components[tp]:

            components_distances[comp1] = {}

            for comp2 in components[tp]:
                distance = 0

                for attr in attrs:
                    if getattr(comp1, attr) != getattr(comp2, attr):
                        distance += 1

                components_distances[comp1][comp2] = distance

    if cache_path:
        with open(cache_file, "wb") as file:
            pickle.dump(components_distances, file)

    return components_distances


def save_components(components, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(components, file)


def load_components(file_path):
    with open(file_path, "rb") as file:
        components = pickle.load(file)

    return components


def get_attributes_names_from_component_type(component_type):
    attrs_names = set(type_to_comp_class_map[component_type].__annotations__) - set(
        Component.__annotations__
    )
    return attrs_names


def get_component_group_key(component, attributes_names=None):
    attributes_values = []

    if not attributes_names:
        attributes_names = attributes_of_interest[component.component_type]

    for attr in attributes_names:
        attr_value = getattr(component, attr)

        if type(attr_value) == list:
            attr_value = tuple(attr_value)

        attributes_values.append((attr, attr_value))

    return tuple(attributes_values)


def group_components_attributes(components, attributes):
    grouped_attributes = {tp: {} for tp in ct}

    for comp_type, comps in components.items():
        for comp in comps:
            comp_group_key = get_component_group_key(comp, attributes[comp_type])

            if comp_group_key not in grouped_attributes[comp_type].keys():
                grouped_attributes[comp_type][comp_group_key] = []

            grouped_attributes[comp_type][comp_group_key].append(comp)

        print(comp_type.name, len(grouped_attributes[comp_type].keys()))

    return grouped_attributes


def convert_components_groups_to_components(grouped_attributes: dict):
    name_pattern = "{comp_type}_group_{n}"
    groups_components = {}

    for comp_type, comp_groups in grouped_attributes.items():
        groups = comp_groups.keys()
        groups_components[comp_type] = []

        for n, group in enumerate(groups):
            group_name = name_pattern.format(comp_type=comp_type.name, n=n)
            attributes = {attr: attr_value for attr, attr_value in group}

            attributes["name"] = group_name

            group_component = create_fake_component(comp_type, **attributes)
            groups_components[comp_type].append(group_component)

    return groups_components
