import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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