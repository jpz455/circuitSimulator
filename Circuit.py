from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from typing import Dict, List

class Circuit:
    def __init__(self,name:str):
        self.name = name
        self.buses: Dict[str, Bus] = dict()
        self.transformers: Dict[str, Transformer] = dict()
        self.geometries: Dict[str, Geometry] = dict()
        self.conductors: Dict[str, Conductor] = dict()
        self.transmissionlines: Dict[str, TransmissionLine] = dict()

    def add_bus(self,bus:Bus):
        # error check if bus already exists in system
        if bus.name in self.buses:
            print(f"Bus with name '{bus.name}' already exists. Skipping addition.")
        else:
            self.buses[bus.name] = bus

    def add_transformer(self,transformer:Transformer):
        if transformer.name in self.transformers:
            print(f"Transformer with name '{transformer.name}' already exists. Skipping addition.")
        else:
            self.transformers[transformer.name] = transformer

    def add_geometry(self,geometry:Geometry):
        if geometry.name in self.geometries:
            print(f"Geometry with name '{geometry.name}' already exists. Skipping addition.")
        else:
            self.geometries[geometry.name] = geometry

    def add_conductor(self,conductor:Conductor):
        if conductor.name in self.conductors:
            print(f"Conductor with name '{conductor.name}' already exists. Skipping addition.")
        else:
            self.conductors[conductor.name] = conductor
    def add_transmissionline(self,transmissionline:TransmissionLine):
        if transmissionline.name in self.transmissionlines:
            print(f"Transmissionline with name '{transmissionline.name}' already exists. Skipping addition.")
        else:
            self.transmissionlines[transmissionline.name] = transmissionline



