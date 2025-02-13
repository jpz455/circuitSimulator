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
            # Retrieve Bus objects using the bus names (or indices) as keys
            bus1 = transmissionline.bus1
            bus2 = transmissionline.bus2
            # Check if the buses have the same base_kv value
            if bus1.base_kv != bus2.base_kv:
                print("ERROR: Cannot connect unmatched voltages for transmission lines.")
                exit(-1)

            # Add the transmission line to the dictionary
            self.transmissionlines[transmissionline.name] = transmissionline

    def calc_ybus(self):
        # Initialize the YBus matrix with size based on the number of buses
        size = np.zeros([len(self.buses), len(self.buses)])
        self.YBus = pd.DataFrame(data=size, index=self.busRef, columns=self.busRef, dtype=complex)

        # update YBus for a given component's admittance matrix
        def update_ybus(yprim, busA, busB):
            # Ensure that yprim is a 2x2 matrix and update YBus correctly

            loc_busA = busA.numBus-1
            loc_busB = busB.numBus-1


            size[loc_busA, loc_busA] += yprim[0]  # ypp
            size[loc_busB, loc_busB] += yprim[3]  # yss
            size[loc_busA, loc_busB] += yprim[1]  # yps
            size[loc_busB, loc_busA] += yprim[2]  # ysp

        #  (Transformer or TransmissionLine)
        def process_component(component):
            # Calculate the primitive admittance matrix
            component.calc_yprim()

            # Retrieve the buses associated with this component
            busA = component.bus1
            busB = component.bus2

            # Update YBus with the calculated admittance matrix
            update_ybus(component.yprim, busA, busB)

        # Process Transformers
        for transformer in self.transformers.values():
            process_component(transformer)

        # Process Transmission Lines
        for transmission_line in self.transmissionlines.values():
            process_component(transmission_line)

        return self.YBus


