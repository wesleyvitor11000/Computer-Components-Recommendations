import json
<<<<<<< HEAD
from .Component import Component, type_to_comp_class_map, ComponentTypes as ct
from pprint import pprint


def import_components_from_file(
    file,
    comp_type: ct,
):
=======
from .Component import Component,type_to_comp_class_map, ComponentTypes as ct
from pprint import pprint


def import_components_from_file(file, comp_type: ct,):
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    json_file = open(file, "r")
    components_dicts = json.load(json_file)
    comp_class = type_to_comp_class_map[comp_type]
    components = []
<<<<<<< HEAD

    for component in components_dicts:
        component_instance = comp_class(**component)
        components.append(component_instance)

=======
    
    for component in components_dicts:
        component_instance = comp_class(**component)
        components.append(component_instance)
    
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    print(len(components), comp_type.name)
    return components


def import_components(
<<<<<<< HEAD
    json_file_pattern=r"res\components\cleaned_data\{0}.json",
    files_variants={
        ct.MOTHERBOARD: "motherboards",
        ct.RAM: "memories",
        ct.SSD: "ssds",
        ct.CPU: "cpus",
        ct.GPU: "gpus",
    },
):

    components = {}
    for comp_type, file_var in files_variants.items():
        components[comp_type] = import_components_from_file(
            json_file_pattern.format(file_var), comp_type
        )
=======
    json_file_pattern = r"res\components\cleaned_data\{0}.json",
    files_variants = {ct.MOTHERBOARD: "motherboards", ct.RAM: "memories", ct.SSD: "ssds", ct.CPU: "cpus", ct.GPU: "gpus"}
):
    
    components = {}
    for comp_type, file_var in files_variants.items():
        components[comp_type] = import_components_from_file(json_file_pattern.format(file_var), comp_type)
        # pprint(components[comp_type])
        # input()
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866

    return components
