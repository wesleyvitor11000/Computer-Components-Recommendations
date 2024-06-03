import json
from .Component import Component,type_to_comp_class_map, ComponentTypes as ct
from pprint import pprint


def import_components_from_file(file, comp_type: ct,):
    json_file = open(file, "r")
    components_dicts = json.load(json_file)
    comp_class = type_to_comp_class_map[comp_type]
    components = []
    
    for component in components_dicts:
        component_instance = comp_class(**component)
        components.append(component_instance)
    
    print(len(components), comp_type.name)
    return components


def import_components(
    json_file_pattern = r"res\components\cleaned_data\{0}.json",
    files_variants = {ct.MOTHERBOARD: "motherboards", ct.RAM: "memories", ct.SSD: "ssds", ct.CPU: "cpus", ct.GPU: "gpus"}
):
    
    components = {}
    for comp_type, file_var in files_variants.items():
        components[comp_type] = import_components_from_file(json_file_pattern.format(file_var), comp_type)
        # pprint(components[comp_type])
        # input()

    return components
