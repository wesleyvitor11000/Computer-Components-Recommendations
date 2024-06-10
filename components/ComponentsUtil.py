from .Component import ComponentTypes as ct, type_to_comp_class_map, Component
from pprint import pprint

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
    ct.GPU: ["is_empty", "pcie"]
}


def create_fake_component(component_type: ct, **kwargs):
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


def get_component_group_key(component, attributes):
    attributes_values = []
    
    for attr in attributes:
        attr_value = getattr(component, attr)
        
        if type(attr_value) == list:
            attr_value = str(attr_value)
            
        attributes_values.append(
            (attr, attr_value)
        )
    
    return tuple(attributes_values)


def group_components_attributes(components, attributes):
    grouped_attributes = {tp: {} for tp in ct}

    for comp_type, comps in components.items():
        for comp in comps:
            comp_group_key = get_component_group_key(comp, attributes[comp_type])

            if comp_group_key not in grouped_attributes[comp_type].keys():
                grouped_attributes[comp_type][comp_group_key] = []

            grouped_attributes[comp_type][comp_group_key].append(comp)

        print(len(grouped_attributes[comp_type].keys()))
    
    return grouped_attributes


def convert_components_groups_to_components(grouped_attributes: dict):
    name_pattern = "{comp_type}_group_{n}"
    groups_components = {}
    
    for comp_type, comp_groups in grouped_attributes.items():
        groups = comp_groups.keys()
        groups_components[comp_type] = []
        
        for n, group in enumerate(groups):
            group_name = name_pattern.format(comp_type = comp_type.name, n = n)
            attributes = {}
            
            for attr, attr_value in group:
                if type(attr_value) == str and len(attr_value) > 0 and attr_value[0] == "[":
                    attr_value = attr_value[1:-1]
                    attr_value = attr_value.split(",")
                    attr_value = [element.replace("'", "") for element in attr_value]
                    # attr_value = [element.replace("'", "").replace(" ", "") for element in attr_value]
                    
                    
                attributes[attr] = attr_value
                
            attributes["name"] = group_name
            
            group_component = create_fake_component(comp_type, **attributes)
            groups_components[comp_type].append(group_component)
    
    return groups_components
            