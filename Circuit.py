from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from typing import Dict, List
from Settings import Settings
from Generator import Generator
from Load import Load
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
        self.transmission_lines: Dict[str, TransmissionLine] = dict()
        self.loads: Dict[str, Load] = dict()
        self.generators: Dict[str, Generator] = dict()
        self.settings: Settings = settings
        self.y_bus: pd.DataFrame = pd.DataFrame()




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

    def add_transmission_line(self, transmission_line: TransmissionLine):
        # Check if the transmission line already exists
        if transmission_line.name in self.transmission_lines:
            print(f"Transmission Line with name '{transmission_line.name}' already exists. Skipping addition.")
        else:

            # Check if the buses have the same base_kv value
            if transmission_line.bus1.base_kv != transmission_line.bus2.base_kv:
                print("ERROR: Cannot connect unmatched voltages for transmission lines.")
                exit(-1)

            # Add the transmission line to the dictionary
            self.transmission_lines[transmission_line.name] = transmission_line

    def add_load(self, load: Load):
        if load.name in self.loads:
            print(f"Load with name '{load.name}' already exists. Skipping addition.")
        else:
            self.loads[load.name] = load

    def add_generator(self, generator: Generator):
            if generator.name in self.generators:
                print(f"Generator with name '{generator.name}' already exists. Skipping addition.")
            else:
                self.generators[generator.name] = generator

    def calc_y_bus(self):
        size = np.zeros([Bus.numBus, Bus.numBus])
        self.y_bus = pd.DataFrame(data=size, index=self.busRef, columns=self.busRef, dtype=complex)



        for yprim in self.transformers.keys():
            self.y_bus.loc[self.transformers[yprim].bus1.name, self.transformers[yprim].bus1.name] += self.transformers[yprim].y_prim_1.loc[self.transformers[yprim].bus1.name, self.transformers[yprim].bus1.name]
            self.y_bus.loc[self.transformers[yprim].bus2.name, self.transformers[yprim].bus2.name] += self.transformers[yprim].y_prim_1.loc[self.transformers[yprim].bus2.name, self.transformers[yprim].bus2.name]
            self.y_bus.loc[self.transformers[yprim].bus1.name, self.transformers[yprim].bus2.name] += self.transformers[yprim].y_prim_1.loc[self.transformers[yprim].bus1.name, self.transformers[yprim].bus2.name]
            self.y_bus.loc[self.transformers[yprim].bus2.name, self.transformers[yprim].bus1.name] += self.transformers[yprim].y_prim_1.loc[self.transformers[yprim].bus2.name, self.transformers[yprim].bus1.name]

        for yprim in self.transmission_lines.keys():
            self.y_bus.loc[self.transmission_lines[yprim].bus1.name, self.transmission_lines[yprim].bus1.name] += self.transmission_lines[yprim].y_prim.loc[self.transmission_lines[yprim].bus1.name, self.transmission_lines[yprim].bus1.name]
            self.y_bus.loc[self.transmission_lines[yprim].bus2.name, self.transmission_lines[yprim].bus2.name] += self.transmission_lines[yprim].y_prim.loc[self.transmission_lines[yprim].bus2.name, self.transmission_lines[yprim].bus2.name]
            self.y_bus.loc[self.transmission_lines[yprim].bus1.name, self.transmission_lines[yprim].bus2.name] += self.transmission_lines[yprim].y_prim.loc[self.transmission_lines[yprim].bus1.name, self.transmission_lines[yprim].bus2.name]
            self.y_bus.loc[self.transmission_lines[yprim].bus2.name, self.transmission_lines[yprim].bus1.name] += self.transmission_lines[yprim].y_prim.loc[self.transmission_lines[yprim].bus2.name, self.transmission_lines[yprim].bus1.name]



        return self.y_bus

    def print_y_bus(self):
        """Prints the Y-bus matrix."""
        if self.y_bus is None:
            print("ERROR: Y-bus has not been calculated yet. Run `calc_ybus()` first.")
        else:
            print("\nY-Bus Matrix:")
            print(self.y_bus.to_string(float_format=lambda x: f"{x:.5f}"))











