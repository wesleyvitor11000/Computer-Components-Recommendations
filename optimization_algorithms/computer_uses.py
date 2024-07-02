from enum import Enum
from components.Component import ComponentTypes as ct


class ComputerUses(Enum):
    GAMING = 0
    STUDY = 1
    PROGRAMMING = 2
    VIDEO_EDITING = 3
    DESIGN = 4
    ENTERTAINMENT = 5
    DEFAULT = 6


components_priorities_by_use = {
    ComputerUses.DEFAULT: {
        ct.MOTHERBOARD: 1,
        ct.RAM: 1,
        ct.SSD: 1,
        ct.GPU: 1,
        ct.CPU: 1,
    },
    ComputerUses.GAMING: {
        ct.MOTHERBOARD: 0.3,
        ct.RAM: 0.4,
        ct.SSD: 0.2,
        ct.GPU: 0.9,
        ct.CPU: 0.8,
    },
    ComputerUses.STUDY: {
        ct.MOTHERBOARD: 0.2,
        ct.RAM: 0.3,
        ct.SSD: 0.3,
        ct.CPU: 0.6,
        ct.GPU: 0.01,
    },
    ComputerUses.PROGRAMMING: {
        ct.MOTHERBOARD: 0.3,
        ct.RAM: 0.4,
        ct.SSD: 0.3,
        ct.CPU: 0.7,
        ct.GPU: 0.1,
    },
    ComputerUses.VIDEO_EDITING: {
        ct.MOTHERBOARD: 0.1,
        ct.RAM: 0.5,
        ct.SSD: 1.5,
        ct.GPU: 2,
        ct.CPU: 1,
    },
    ComputerUses.DESIGN: {
        ct.MOTHERBOARD: 0.3,
        ct.RAM: 0.4,
        ct.SSD: 0.3,
        ct.GPU: 0.7,
        ct.CPU: 0.6,
    },
    ComputerUses.ENTERTAINMENT: {
        ct.MOTHERBOARD: 0.2,
        ct.RAM: 0.3,
        ct.SSD: 0.2,
        ct.GPU: 0.4,
        ct.CPU: 0.5,
    },
}


def get_normalized_priorities(computer_use: ComputerUses):
    priorities = components_priorities_by_use[computer_use]
    priorities_sum = sum(priorities.values())

    normalized_priorities = {tp: priorities[tp] / priorities_sum for tp in ct}

    return normalized_priorities
