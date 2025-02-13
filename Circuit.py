import numpy as np
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

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

    def calc_ybus(self):
        #set n as number of buses
        n = self.buses.__sizeof__()

        #intialize matrix of zeroes of size n
        y_matrix = np.zeros(n)

        #get all y_prims from transmission lines and transformers
        #start by getting names of buses from buses dictionary
        bus_names = []
        bus_0 = []
        bus_1 = []
        bus_2 = []
        bus_3 = []
        bus_4 = []
        bus_5 = []
        bus_6 = []
        for bus in self.buses.values():
            bus_names.append(bus.name)

        #next loop through transmission lines and find buses that match lines; add y matrix
        for line in self.transmissionlines.values():
            line.calculate_y_matrix()
            if line.bus1_key == bus_names[0]:
                bus_0.append(line.matrix)
            elif line.bus1_key == bus_names[1]:
                bus_1.append(line.matrix)
            elif line.bus1_key == bus_names[2]:
                bus_2.append(line.matrix)
            elif line.bus1_key == bus_names[3]:
                bus_3.append(line.matrix)
            elif line.bus1_key == bus_names[4]:
                bus_4.append(line.matrix)
            elif line.bus1_key == bus_names[5]:
                bus_5.append(line.matrix)
            elif line.bus1_key == bus_names[6]:
                bus_6.append(line.matrix)
            else:
                print("No bus found.")

            if line.bus2_key == bus_names[0]:
                bus_0.append(line.matrix)
            elif line.bus2_key == bus_names[1]:
                bus_1.append(line.matrix)
            elif line.bus2_key == bus_names[2]:
                bus_2.append(line.matrix)
            elif line.bus2_key == bus_names[3]:
                bus_3.append(line.matrix)
            elif line.bus2_key == bus_names[4]:
                bus_4.append(line.matrix)
            elif line.bus2_key == bus_names[5]:
                bus_5.append(line.matrix)
            elif line.bus2_key == bus_names[6]:
                bus_6.append(line.matrix)
            else:
                print("No bus found.")

        for xfmr in self.transformers.values():
            xfmr.calc_yprim()
            if xfmr.bus1 == bus_names[0]:
                bus_0.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[1]:
                bus_1.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[2]:
                bus_2.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[3]:
                bus_3.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[4]:
                bus_4.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[5]:
                bus_5.append(xfmr.matrix)
            elif xfmr.bus1 == bus_names[6]:
                bus_6.append(xfmr.matrix)
            else:
                print("No bus found.")

            if xfmr.bus2 == bus_names[0]:
                bus_0.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[1]:
                bus_1.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[2]:
                bus_2.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[3]:
                bus_3.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[4]:
                bus_4.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[5]:
                bus_5.append(xfmr.matrix)
            elif xfmr.bus2 == bus_names[6]:
                bus_6.append(xfmr.matrix)
            else:
                print("No bus found.")

           """""
            #debugging
            print()
            print("Here are my values for each bus:")
            print(bus_0)
            print(bus_1)
            print(bus_2)
            print(bus_3)
            print(bus_4)
            print(bus_5)
            print(bus_6)
         
            """""

            #now have to add correct elements
        diagonals_0 = 0
        off_diagonals_0 = 0
        for matrix in bus_0:
            diagonals_0 = diagonals_0 + matrix[0,0] + matrix[1,1]
            off_diagonals_0 = off_diagonals_0 + matrix[0,1] + matrix[1,0]

        diagonals_1 = 0
        off_diagonals_1 = 0
        for matrix in bus_1:
            diagonals_1 = diagonals_1 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_1 = off_diagonals_1 + matrix[0, 1] + matrix[1, 0]

        diagonals_2 = 0
        off_diagonals_2 = 0
        for matrix in bus_2:
            diagonals_2 = diagonals_2 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_2 = off_diagonals_2 + matrix[0, 1] + matrix[1, 0]

        diagonals_3 = 0
        off_diagonals_3 = 0
        for matrix in bus_3:
            diagonals_3 = diagonals_3 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_3 = off_diagonals_3 + matrix[0, 1] + matrix[1, 0]

        diagonals_4 = 0
        off_diagonals_4 = 0
        for matrix in bus_4:
            diagonals_4 = diagonals_4 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_4 = off_diagonals_4 + matrix[0, 1] + matrix[1, 0]

        diagonals_5 = 0
        off_diagonals_5 = 0
        for matrix in bus_5:
            diagonals_5 = diagonals_5 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_5 = off_diagonals_5 + matrix[0, 1] + matrix[1, 0]

        diagonals_6 = 0
        off_diagonals_6 = 0
        for matrix in bus_4:
            diagonals_6 = diagonals_6 + matrix[0, 0] + matrix[1, 1]
            off_diagonals_6 = off_diagonals_6 + matrix[0, 1] + matrix[1, 0]




