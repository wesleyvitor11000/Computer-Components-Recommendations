from enum import IntEnum
import uuid
<<<<<<< HEAD
from dataclasses import dataclass, field
=======
from dataclasses import dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866


class ComponentTypes(IntEnum):
    MOTHERBOARD = 0
    RAM = 1
    SSD = 2
    CPU = 3
    GPU = 4


<<<<<<< HEAD
@dataclass(kw_only=True, frozen=True, eq=False)
class Component:
=======
@dataclass
class Component:
    uid = uuid.uuid4()
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
    name: str
    mark: int
    link: str
    price: float
<<<<<<< HEAD
    uid: int = field(default_factory=uuid.uuid4)
    is_empty: bool = field(default=False)
    component_type = None
    
    def __hash__(self) -> int:
        return hash(str(self.uid))
    
        
@dataclass(kw_only=True, frozen=True, eq=False)
=======

        
@dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
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
<<<<<<< HEAD
    pci_slots: tuple[str]
    component_type=ComponentTypes.MOTHERBOARD
    
    
@dataclass(kw_only=True, frozen=True, eq=False)
=======
    pci_slots: list[str]
    
    
@dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
class Ram(Component):
    memory_speed: int
    ddr_version: int
    memory_size: int
    total_ram_size: int
    memory_form_factor: str
    memory_modules: int
<<<<<<< HEAD
    component_type=ComponentTypes.RAM


@dataclass(kw_only=True, frozen=True, eq=False)
=======


@dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
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
<<<<<<< HEAD
    component_type=ComponentTypes.SSD
    
        
@dataclass(kw_only=True, frozen=True, eq=False)
=======
    
        
@dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
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
<<<<<<< HEAD
    component_type=ComponentTypes.CPU
    

@dataclass(kw_only=True, frozen=True, eq=False)
=======
    

@dataclass
>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866
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
<<<<<<< HEAD
    component_type=ComponentTypes.GPU
=======

>>>>>>> 7d96dbbfbc4c303d1624387f1b28394699a94866


type_to_comp_class_map = {
    ComponentTypes.MOTHERBOARD: Motherboard,
    ComponentTypes.RAM: Ram,
    ComponentTypes.SSD: SSD,
    ComponentTypes.CPU: CPU,
    ComponentTypes.GPU: GPU,
}
