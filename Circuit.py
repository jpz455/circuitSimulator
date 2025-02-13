from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from typing import Dict, List
from Settings import Settings
import numpy as np
import pandas as pd

class Circuit:
    def __init__(self,name:str, settings: Settings):
        self.name = name
        self.buses: Dict[str, Bus] = dict()
        self.busRef :List[str] = list()
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
            self.busRef.append(bus.name)

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

            # Check if the buses have the same base_kv value
            if transmissionline.bus1.base_kv != transmissionline.bus2.base_kv:
                print("ERROR: Cannot connect unmatched voltages for transmission lines.")
                exit(-1)

            # Add the transmission line to the dictionary
            self.transmissionlines[transmissionline.name] = transmissionline

    def calc_ybus(self):
        size = np.zeros([Bus.numBus, Bus.numBus])
        self.YBus = pd.DataFrame(data=size, index=self.busRef, columns=self.busRef, dtype=complex)

        for A in self.transformers.keys():
            self.YBus.loc[self.transformers[A].bus1.name, self.transformers[A].bus1.name] += self.transformers[A].yprim.loc[self.transformers[A].bus1.name, self.transformers[A].bus1.name]
            self.YBus.loc[self.transformers[A].bus2.name, self.transformers[A].bus2.name] += self.transformers[A].yprim.loc[self.transformers[A].bus2.name, self.transformers[A].bus2.name]
            self.YBus.loc[self.transformers[A].bus1.name, self.transformers[A].bus2.name] += self.transformers[A].yprim.loc[self.transformers[A].bus1.name, self.transformers[A].bus2.name]
            self.YBus.loc[self.transformers[A].bus2.name, self.transformers[A].bus1.name] += self.transformers[A].yprim.loc[self.transformers[A].bus2.name, self.transformers[A].bus1.name]

        for A in self.transmissionlines.keys():
            self.YBus.loc[self.transmissionlines[A].bus1.name, self.transmissionlines[A].bus1.name] += self.transmissionlines[A].yprim.loc[self.transmissionlines[A].bus1.name, self.transmissionlines[A].bus1.name]
            self.YBus.loc[self.transmissionlines[A].bus2.name, self.transmissionlines[A].bus2.name] += self.transmissionlines[A].yprim.loc[self.transmissionlines[A].bus2.name, self.transmissionlines[A].bus2.name]
            self.YBus.loc[self.transmissionlines[A].bus1.name, self.transmissionlines[A].bus2.name] += self.transmissionlines[A].yprim.loc[self.transmissionlines[A].bus1.name, self.transmissionlines[A].bus2.name]
            self.YBus.loc[self.transmissionlines[A].bus2.name, self.transmissionlines[A].bus1.name] += self.transmissionlines[A].yprim.loc[self.transmissionlines[A].bus2.name, self.transmissionlines[A].bus1.name]

        return self.YBus

    def print_ybus(self):
        """Prints the Y-bus matrix."""
        if self.YBus is None:
            print("ERROR: Y-bus has not been calculated yet. Run `calc_ybus()` first.")
        else:
            print("\nY-Bus Matrix:")
            print(self.YBus.to_string(float_format=lambda x: f"{x:.5f}"))



