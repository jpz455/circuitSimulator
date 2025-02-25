from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings
from TransmissionLine import TransmissionLine as TransmissionLine
import numpy as np
from Transformer import Transformer
from Circuit import Circuit as Circuit



#************TRANSFORMER VALIDATION***********************#
#
# bus1 = Bus("Bus 1", 20, "Slack")
# bus2 = Bus("Bus 2", 230, "PQ")
# xfmr1 = Transformer("T1", bus1, bus2, 124, 8.5, 10)
# print("Transformer Validation")
# print("name: ", xfmr1.name, "; should be T1")
# print("bus1: ", xfmr1.bus1, "; should be Bus 1")
# print("bus2: ", xfmr1.bus2, "; should be Bus 2")
# print("power rating: ", xfmr1.power_rating, "; should be 124")
# print("impedance percent: ", xfmr1.impedance_percent, "; should be 8.5")
# print("ratio: ", xfmr1.x_over_r_ratio, "; should be 10")
# #**********CONDUCTOR VALIDATION******************
# conductor1 = Conductor("Partridge", 0.642, 0.0217,0.385, 460)
# print()
# print("Conductor Validation")
# print("name:", conductor1.name, ";should be Partridge")
# print("diameter:", conductor1.diameter, ";should be 0.642")
# print("GMR:", conductor1.GMR, ";should be 0.0217")
# print("resistance:", conductor1.resistance, ";should be 0.385")
# print("amperage:", conductor1.amp, ";should be 460")
# print()


#*********BUS VALIDATION**************************

print("Bus Validation")
bus1 = Bus("Bus 1", 20, "Slack")
bus2 = Bus("Bus 2", 230, "PQ")
print("bus1 name:", bus1.name, "; should be Bus 1")
print("bus1 base voltage:", bus1.base_kv, ";should be 20")
print("bus1 index:", bus1.index, "; should be 1")
print("bus1 type:", bus1.bus_type, "; should be Slack")
print("bus1 vpu:", bus1.v_pu, "; should be 1.0")
print("bus1 delta:", bus1.delta, "; should be 0.0")


print("bus2 name:", bus2.name, "; should be Bus 2")
print("bus 2 base voltage:", bus2.base_kv, ";should be 230")
print("bus 2 index: ", bus2.index, "; should be 2")
print("bus2 type:", bus2.bus_type, "; should be PQ")
print("bus2 vpu:", bus2.v_pu, "; should be 1.0")
print("bus2 delta:", bus2.delta, "; should be 0.0")
print()

"""""
#************BUNDLE VALIDATION**********************
print("Bundle Validation")
bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(bundle1.name, bundle1.num_conductors,bundle1.spacing, bundle1.conductor.name)
print("bundle1 name:", bundle1.name, "; should be Bundle 1")
print("bundle1 num conductors:", bundle1.num_conductors, "; should be 2")
print("bundle1 spacing:", bundle1.spacing, "; should be 1.5")
print("bundle1 DSC:", bundle1.DSC)
print("bundle1 DSL:", bundle1.DSL)
print()
#*********GEOMETRY VALIDATION***************
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0,37, 0)
print("Geometry Validation")
print("Geometry 1 name:", geometry1.name, "; should be Geometry 1")
print("Geometry 1 xa:", geometry1.xa, "; should be 0")
print("Geometry 1 ya:", geometry1.ya, "; should be 0")
print("Geometry 1 xb:", geometry1.xb, "; should be 18.5")
print("Geometry 1 yb:", geometry1.yb, "; should be 0")
print("Geometry 1 xc:", geometry1.xc, "; should be 37")
print("Geometry 1 yc:", geometry1.yc, "; should be 0")
print("Geometry 1 Deq:", geometry1.Deq)
print()
#*******************TRANSMISSION LINE VALIDATION************
line1 = TransmissionLine("Line 1", bus1, bus2,bundle1, geometry1, 10)
print("TransmissionLine Validation")
print("Line 1 name:", line1.name, "; should be Line 1")
print("Line 1 length:", line1.length, "; should be 10")
print("Line 1 Z:", line1.Zpu)
print("Line 1 Y:", line1.Ypu)
print("Line 1 B:", line1.Bpu)
line1.print_yprim()
print()
"""""
#************************CIRCUIT VALIDATION****************************#
# Create circuit instance
circuit1 = Circuit("Test Circuit", current_settings)

print(circuit1.name)  # Expected output: "Test Circuit"
print(type(circuit1.name))  # Expected output: <class 'str'>
print(circuit1.buses)  # Expected output: {}
print(type(circuit1.buses))  # Expected output: <class 'dict'>

# Correct way to add a bus
bus1 = Bus("Bus1", 20, "Slack")
bus2 = Bus("Bus2", 20, "PQ")
bus3 = Bus('Bus3', 20, "PQ")
bus4 = Bus("Bus4", 20, "PQ")
bus5 = Bus("Bus5", 20, "PQ")
bus6 = Bus("Bus6", 20, "PQ")
bus7 = Bus("Bus7", 20, "PV")
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

