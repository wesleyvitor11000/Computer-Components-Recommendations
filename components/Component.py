from enum import IntEnum
import uuid
from dataclasses import dataclass


class ComponentTypes(IntEnum):
    MOTHERBOARD = 0
    RAM = 1
    SSD = 2
    CPU = 3
    GPU = 4


@dataclass
class Component:
    uid = uuid.uuid4()
    name: str
    mark: int
    link: str
    price: float

        
@dataclass
class Motherboard(Component):
    socket: str
    chipset: str
    form_factor: str
    max_memory: int
    ram_speed: int
    memory_slots: int
    ddr_version: int
    memory_channels: int
    sata3_connectors: int
    m2_sockets: int
    u2_sockets: int
    pcie4_x16_slots: int
    pcie5_x16_slots: int
    pcie3_x16_slots: int
    pcie_x1_slots:int
    pci_l_slots: int
    pcie2_x16_slots: int
    pcie_x4_slots: int
    pcie_x8_slots: int
    pci_slots: list[str]
    
    
@dataclass
class Ram(Component):
    memory_speed: int
    ddr_version: int
    memory_size: int
    total_ram_size: int
    memory_form_factor: str
    memory_modules: int


@dataclass
class SSD(Component):
    max_read_sequential: int
    read_random: int
    max_write_sequential: int
    write_random: int
    ssd_format: str
    nvme: bool
    pcie: int
    tbw: int
    internal_storage: int
    
        
@dataclass
class CPU(Component):
    cpu_type: str
    cpu_socket: str
    compatible_chipsets: list[str]
    integrated_graphics: bool
    pcie: str
    cpu_threads: int
    turbo_clock: float
    l1_cache: int
    l2_cache: int
    l3_cache: int
    ram_speed_max: int
    max_mem_bandwidth: float
    ddr_version: int
    mem_channels: int
    max_mem_size: int
    passmark: int
    

@dataclass
class GPU(Component):
    gpu_clock_speed: float
    gpu_turbo: float
    gpu_memory_speed: int
    gpu_ram: int
    gddr_version: str
    directx_version: str
    opengl_version: str
    ray_tracing: bool
    dlss: bool
    gpu_displays: int
    hdmi: bool
    hdmi_ports: int
    hdmi_version: str
    displayport: bool
    ports_usb_c: int
    dvi: bool
    mini_displayport: bool
    pcie: str



type_to_comp_class_map = {
    ComponentTypes.MOTHERBOARD: Motherboard,
    ComponentTypes.RAM: Ram,
    ComponentTypes.SSD: SSD,
    ComponentTypes.CPU: CPU,
    ComponentTypes.GPU: GPU,
}
