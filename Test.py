from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings
from TransmissionLine import TransmissionLine as TransmissionLine
import numpy as np
from Transformer import Transformer
from Circuit import Circuit as Circuit

# Create circuit instance
circuit1 = Circuit("Test Circuit", current_settings)

# add bus
bus1 = Bus("Bus1", 20, "Slack")
bus2 = Bus("Bus2", 230, "PQ")
bus3 = Bus('Bus3', 230, "PQ")
bus4 = Bus("Bus4", 230, "PQ")
bus5 = Bus("Bus5", 230, "PQ")
bus6 = Bus("Bus6", 230, "PQ")
bus7 = Bus("Bus7", 18, "PV")

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
transformer1 = Transformer('XFMR1', bus1, bus2, 100, 80, 2)
transformer2 = Transformer('XFMR2', bus6, bus7, 150, 90, 3)
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
circuit1.add_transmission_line(transmissionLine1)
circuit1.add_transmission_line(transmissionLine2)
circuit1.add_transmission_line(transmissionLine3)
circuit1.add_transmission_line(transmissionLine4)
circuit1.add_transmission_line(transmissionLine5)
circuit1.add_transmission_line(transmissionLine6)

