from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from typing import Dict, List
from Settings import Settings

class Circuit:
    def __init__(self,name:str, settings: Settings):
        self.name = name
        self.buses: Dict[str, Bus] = dict()
        self.transformers: Dict[str, Transformer] = dict()
        self.geometries: Dict[str, Geometry] = dict()
        self.conductors: Dict[str, Conductor] = dict()
        self.transmissionlines: Dict[str, TransmissionLine] = dict()
        self.settings: Settings = settings

    def add_bus(self, bus: Bus):
        # Check if bus already exists in system
        if bus.name in self.buses:
            print(f"Bus with name '{bus.name}' already exists. Skipping addition.")
        else:
            self.buses[bus.name] = bus  # Add bus to the dictionary using its name as the key



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

    def add_transmissionline(self, transmissionline: TransmissionLine):
        # Check if the transmission line already exists
        if transmissionline.name in self.transmissionlines:
            print(f"Transmissionline with name '{transmissionline.name}' already exists. Skipping addition.")
        else:
            # Retrieve Bus objects using the bus names (or indices) as keys
            bus1 = self.buses.get(transmissionline.bus1_key)
            bus2 = self.buses.get(transmissionline.bus2_key)

            # Ensure both buses are found
            if bus1 is None or bus2 is None:
                print(
                    f"ERROR: One or both buses not found. Bus1: {transmissionline.bus1_key}, Bus2: {transmissionline.bus2_key}")
                exit(-1)

            # Check if the buses have the same base_kv value
            if bus1.base_kv != bus2.base_kv:
                print("ERROR: Cannot connect unmatched voltages for transmission lines.")
                exit(-1)

            # Add the transmission line to the dictionary
            self.transmissionlines[transmissionline.name] = transmissionline





