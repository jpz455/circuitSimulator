from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from Bundle import Bundle
from typing import Dict

class Circuit:
    def __init__(self, name: str):
        self.name = name
        self.buses: Dict[str, Bus] = {}
        self.transformers: Dict[str, Transformer] = {}
        self.geometries: Dict[str, Geometry] = {}
        self.conductors: Dict[str, Conductor] = {}
        self.transmissionlines: Dict[str, TransmissionLine] = {}

    def add_bus(self, bus: Bus):
        if bus.name in self.buses:
            print(f"Bus with name '{bus.name}' already exists. Skipping addition.")
        else:
            self.buses[bus.name] = bus

    def add_transformer(self, transformer: Transformer):
        if transformer.name in self.transformers:
            print(f"Transformer with name '{transformer.name}' already exists. Skipping addition.")
        else:
            self.transformers[transformer.name] = transformer

    def add_geometry(self, geometry: Geometry):
            self.geometries[geometry.name] = geometry

    def add_conductor(self, conductor: Conductor):
            self.conductors[conductor.name] = conductor

    def add_transmissionline(self, transmissionline: TransmissionLine):
        if transmissionline.name in self.transmissionlines:
            print(f"Transmission line with name '{transmissionline.name}' already exists. Skipping addition.")
        else:
            self.transmissionlines[transmissionline.name] = transmissionline



# Create circuit instance
circuit1 = Circuit("Test Circuit")

print(circuit1.name)  # Expected output: "Test Circuit"
print(type(circuit1.name))  # Expected output: <class 'str'>
print(circuit1.buses)  # Expected output: {}
print(type(circuit1.buses))  # Expected output: <class 'dict'>

# Correct way to add a bus
bus1 = Bus("Bus1", 230)
bus2 = Bus("Bus2", 130)
bus3 = Bus('Bus3', 200)
bus4 = Bus("Bus4", 150)
bus5 = Bus("Bus5", 20)
bus6 = Bus("Bus6", 2300000)
bus7 = Bus("Bus7", 2460)
circuit1.add_bus(bus1)
circuit1.add_bus(bus2)
circuit1.add_bus(bus3)
circuit1.add_bus(bus4)
circuit1.add_bus(bus5)
circuit1.add_bus(bus6)
circuit1.add_bus(bus7)
print(type(circuit1.buses["Bus1"]))  # Expected output: <class 'Bus'>
print(circuit1.buses["Bus1"].name, circuit1.buses["Bus1"].base_kv)  # Expected output: "Bus1", 230
print("Buses in circuit:", list(circuit1.buses.keys())) #
transformer1 = Transformer('XFMR1', 'Bus1', 'Bus2', 100, 80, 2)
transformer2 = Transformer('XFMR2', 'Bus6', 'Bus7', 150, 90, 3)
circuit1.add_transformer(transformer1)
circuit1.add_transformer(transformer2)
Geometry1 = Geometry('G1',.2,.2,3,0,.9,.1)
Geometry2 = Geometry('G2',.5,.1,.7,.9,.2,.1)
Conductor1 = Conductor('C1',.2,.1,3,100)
Bundle1 = Bundle('B1',3,2,Conductor1)
transmissionLine1 = TransmissionLine('TL1',bus2,bus4,Bundle1,Geometry1,100)
transmissionLine2 = TransmissionLine('TL2',bus2,bus3,Bundle1,Geometry1,100)
transmissionLine3 = TransmissionLine('TL3',bus3,bus5,Bundle1,Geometry1,100)
transmissionLine4 = TransmissionLine('TL4',bus4,bus5,Bundle1,Geometry1,100)
transmissionLine5 = TransmissionLine('TL5',bus5,bus6,Bundle1,Geometry1,100)
transmissionLine6 = TransmissionLine('TL6',bus4,bus5,Bundle1,Geometry1,100)
circuit1.add_transmissionline(transmissionLine1)
circuit1.add_transmissionline(transmissionLine2)
circuit1.add_transmissionline(transmissionLine3)
circuit1.add_transmissionline(transmissionLine4)
circuit1.add_transmissionline(transmissionLine5)
circuit1.add_transmissionline(transmissionLine6)


