from .VersusScraper import ElementSource

"""
    {
        component_type: {
            element_type:{
                atribute: [element_value, steps_forward, high_priority, source]
            }
        }
    }
"""

data_to_colect_by_comp_type = {
    "motherboard": {
        "class": {
<<<<<<< HEAD
            "price": [
                "natural",
                0,
                True,
            ]
        },
        "href": {
            "socket": [
                "/en/{name}/cpu-socket",
                3,
                False,
            ],
            "chipset": [
                "/en/{name}/compatible-chipsets",
                3,
                False,
            ],
            "form_factory": [
                "/en/{name}/form-factor",
                3,
                False,
            ],
            "max_memory": [
                "/en/{name}/max-mem-size",
                3,
                False,
            ],
            "ram_speed": [
                "/en/{name}/ram-speed-mb-max",
                3,
                False,
            ],
            "memory_slots": [
                "/en/{name}/memory-slots",
                3,
                False,
            ],
            "ddr_version": [
                "/en/{name}/ddr-version",
                3,
                False,
            ],
            "memory_channels": [
                "/en/{name}/mem-channels",
                3,
                False,
            ],
            "sata3_connectors": [
                "/en/{name}/sata3-connectors",
                3,
                False,
            ],
            "m2_sockets": [
                "/en/{name}/m2-sockets",
                3,
                False,
            ],
            "u2_sockets": [
                "/en/{name}/u2-sockets",
                3,
                False,
            ],
            "sata2_connectors": [
                "/en/{name}/sata2-connectors",
                3,
                False,
            ],
            "pcie4_x16-slots": [
                "/en/{name}/pcie4-x16-slots",
                3,
                False,
            ],
            "pcie5_x16-slots": [
                "/en/{name}/pcie5-x16-slots",
                3,
                False,
            ],
            "pcie3_x16-slots": [
                "/en/{name}/pcie3-x16-slots",
                3,
                False,
            ],
            "pcie_x1_slots": [
                "/en/{name}/pcie-x1-slots",
                3,
                False,
            ],
            "pci_l_slots": [
                "/en/{name}/pci-l-slots",
                3,
                False,
            ],
            "pcie2_x16_slots": [
                "/en/{name}/pcie2-slots",
                3,
                False,
            ],
            "pcie_x4_slots": [
                "/en/{name}/pcie-x4-slots",
                3,
                False,
            ],
            "pcie_x8_slots": [
                "/en/{name}/pcie-x8-slots",
                3,
                False,
            ],
=======
            "price": ["natural", 0, True, ]
        },
        "href": {
            "socket": ["/en/{name}/cpu-socket", 3, False,],
            "chipset": ["/en/{name}/compatible-chipsets", 3, False,],
            "form_factory": ["/en/{name}/form-factor", 3, False,],
            "max_memory": ["/en/{name}/max-mem-size", 3, False,],
            "ram_speed": ["/en/{name}/ram-speed-mb-max", 3, False,],
            "memory_slots": ["/en/{name}/memory-slots", 3, False,],
            "ddr_version": ["/en/{name}/ddr-version", 3, False,],
            "memory_channels": ["/en/{name}/mem-channels", 3, False,],
            "sata3_connectors": ["/en/{name}/sata3-connectors",3,False,],
            "m2_sockets": ["/en/{name}/m2-sockets",3,False,],
            "u2_sockets": ["/en/{name}/u2-sockets",3,False,],
            "sata2_connectors": ["/en/{name}/sata2-connectors",3,False,],
            "pcie4_x16-slots": ["/en/{name}/pcie4-x16-slots",3,False,],
            "pcie5_x16-slots": ["/en/{name}/pcie5-x16-slots",3,False,],
            "pcie3_x16-slots": ["/en/{name}/pcie3-x16-slots",3,False,],
            "pcie_x1_slots": ["/en/{name}/pcie-x1-slots",3,False,],
            "pci_l_slots": ["/en/{name}/pci-l-slots",3,False,],
            "pcie2_x16_slots": ["/en/{name}/pcie2-slots",3,False,],
            "pcie_x4_slots": ["/en/{name}/pcie-x4-slots",3,False,],
            "pcie_x8_slots": ["/en/{name}/pcie-x8-slots",3,False,],
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
        },
    },
    "memory": {
        "class": {"price": ["natural", 0, True]},
        "href": {
            "memory_speed": ["/en/{name}/memory-speed-spd", 3, False],
            "ddr_version": ["/en/{name}/ddr-version", 3, False],
            "memory_size": ["/en/{name}/ram-module-size", 3, False],
            "total_ram_size": ["/en/{name}/total-ram-size", 3, False],
            "form_factor": ["/en/{name}/memory-form-factor", 3, False],
            "ubm_bench": ["/en/{name}/ubm-bench", 3, False],
        },
    },
    "ssd": {
        "class": {"price": ["natural", 0, True]},
        "href": {
            "max_read_sequential": ["/en/{name}/max-read-sequential", 3, False],
            "read_random": ["/en/{name}/read-random", 3, False],
            "max_write_sequential": ["/en/{name}/max-write-sequential", 3, False],
            "write_random": ["/en/{name}/write-random", 3, False],
            "passmark_ssd": ["/en/{name}/passmark-ssd", 3, False],
            "ssd_format": ["/en/{name}/ssd-format", 3, False],
            "nvme": ["/en/{name}/nvme", 5, False],
            "pcie": ["/en/{name}/pcie", 3, False],
            "tbw": ["/en/{name}/tbw", 3, False],
            "internal_storage": ["/en/{name}/internal-storage", 3, False],
        },
    },
    "graphics-card": {
        "class": {"price": ["natural", 0, True]},
        "href": {
            "gpu_clock_speed": ["/en/{name}/gpu-clock-speed", 3, False],
            "gpu_turbo": ["/en/{name}/gpu-turbo", 3, False],
            "gpu_memory_speed": ["/en/{name}/gpu-memory-speed", 3, False],
            "gpu_ram": ["/en/{name}/gpu-ram", 3, False],
            "gddr_version": ["/en/{name}/gddr-version-r", 3, False],
            "directx_version": ["/en/{name}/directx-version-r", 3, False],
            "opengl_version": ["/en/{name}/opengl-version", 3, False],
            "ray_tracing": ["/en/{name}/ray-tracing", 5, False],
            "dlss": ["/en/{name}/dlss", 5, False],
            "gpu_displays": ["/en/{name}/gpu-displays", 3, False],
            "hdmi": ["/en/{name}/hdmi", 5, False],
            "hdmi_ports": ["/en/{name}/hdmi-ports", 3, False],
            "hdmi_version": ["/en/{name}/hdmi-version-r", 3, False],
            "displayport": ["/en/{name}/displayport", 3, False],
            "ports_usb_c": ["/en/{name}/ports-usb-c", 3, False],
            "dvi": ["/en/{name}/dvi", 3, False],
            "mini-displayport": ["/en/{name}/mini-displayport", 3, False],
            "pcie": ["/en/{name}/pcie", 3, False],
        },
    },
    "cpu": {
        "class": {"price": ["natural", 0, True]},
        "href": {
            "cpu_type": ["/en/{name}/cpu-type", 3, False],
            "cpu_socket": ["/en/{name}/cpu-socket", 3, False],
            "compatible_chipsets": ["/en/{name}/compatible-chipsets", 3, False],
            "integrated_graphics": ["/en/{name}/int-graphics", 5, False],
            "pcie": ["/en/{name}/pcie", 3, False],
            "total_clock_speed": ["/en/{name}/total-clock-speed", 3, False],
            "cpu_threads": ["/en/{name}/cpu-threads", 3, False],
            "turbo_clock": ["/en/{name}/turbo", 3, False],
            "l1_cache": ["/en/{name}/l1-cache", 3, False],
            "l2_cache": ["/en/{name}/l2-cache", 3, False],
            "l3_cache": ["/en/{name}/l3-cache", 3, False],
            "ram_speed_max": ["/en/{name}/ram-speed-max", 3, False],
            "max_mem_bandwidth": ["/en/{name}/max-mem-bandwidth", 3, False],
            "ddr_version": ["/en/{name}/ddr-version", 3, False],
            "mem_channels": ["/en/{name}/mem-channels", 3, False],
            "max_mem_size": ["/en/{name}/max-mem-size", 3, False],
            "passmark": ["/en/{name}/passmark", 3, False],
        },
    },
}
