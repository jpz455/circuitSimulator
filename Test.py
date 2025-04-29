from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings
from TransmissionLine import TransmissionLine as TransmissionLine
import numpy as np
from Transformer import Transformer
from Circuit import Circuit as Circuit
from Load import Load as Load
from Generator import Generator as Generator
from Solution import Solution
from Fault import Fault

# Circuit
circuit1 = Circuit("Test Circuit", current_settings)

# Bus
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

# Transformers
transformer1 = Transformer('XFMR1', bus1, bus2, 125, 8.5, 10, 'delta-y', 1)
transformer2 = Transformer('XFMR2', bus6, bus7, 200, 10.5, 12,'delta-y',0)
circuit1.add_transformer(transformer1)
circuit1.add_transformer(transformer2)

conductor1 = Conductor("Partridge",.642,.0217,.385,460)
circuit1.add_conductor(conductor1)

# Geometry and Bundle
geometry1 = Geometry("G1",0,0,19.5,0,39,0)
circuit1.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)

# Lines
transmissionLine1 = TransmissionLine("tline1",bus2, bus4,bundle1,geometry1,10)
transmissionLine2 = TransmissionLine("tline2",bus2, bus3,bundle1,geometry1,25)
transmissionLine3 = TransmissionLine("tline3",bus3, bus5,bundle1,geometry1,20)
transmissionLine4 = TransmissionLine("tline4",bus4, bus6,bundle1,geometry1,20)
transmissionLine5 = TransmissionLine("tline5",bus5, bus6,bundle1,geometry1,10)
transmissionLine6 = TransmissionLine("tline6",bus4, bus5,bundle1,geometry1,35)
circuit1.add_transmission_line(transmissionLine1)
circuit1.add_transmission_line(transmissionLine2)
circuit1.add_transmission_line(transmissionLine3)
circuit1.add_transmission_line(transmissionLine4)
circuit1.add_transmission_line(transmissionLine5)
circuit1.add_transmission_line(transmissionLine6)

# Loads
load3 = Load("load3",bus3,-110,-50, current_settings)
circuit1.add_load(load3)
load4 = Load("load4",bus4,-100,-70, current_settings)
circuit1.add_load(load4)
load5 = Load("load5",bus5,-100,-65, current_settings)
circuit1.add_load(load5)

# Generators
gen1 = Generator("Gen 1",bus1,0,100, .12,.14,.05,0,True, current_settings)
circuit1.add_generator(gen1)
gen2 = Generator("Gen 2",bus7,0,200, .12,.14,.05,0.01,True, current_settings)
circuit1.add_generator(gen2)

# Solution
solver = Solution(circuit1)


# Y Buses
circuit1.calc_y_bus_positive()
circuit1.calc_y_bus_negative()
circuit1.calc_y_bus_zero()
circuit1.calc_y_bus_no_gen()

# Faults
fault = Fault(circuit1)

# Print
print("Transformers")
print("xfmr 1: r, x, y:", transformer1.r_pu, transformer1.x_pu, transformer1.y_pu)
print("xfmr 2: r, x, y:", transformer2.r_pu, transformer2.x_pu, transformer2.y_pu)
print()

print("Lines")
print("tline 1: r, x, b:", transmissionLine1.r_pu, transmissionLine1.x_pu, transmissionLine1.y_shunt_pu)
print("tline 2: r, x, b:", transmissionLine2.r_pu, transmissionLine2.x_pu, transmissionLine2.y_shunt_pu)
print("tline 3: r, x, b:", transmissionLine3.r_pu, transmissionLine3.x_pu, transmissionLine3.y_shunt_pu)
print("tline 4: r, x, b:", transmissionLine4.r_pu, transmissionLine4.x_pu, transmissionLine4.y_shunt_pu)
print("tline 5: r, x, b:", transmissionLine5.r_pu, transmissionLine5.x_pu, transmissionLine5.y_shunt_pu)
print("tline 6: r, x, b:", transmissionLine6.r_pu, transmissionLine6.x_pu, transmissionLine6.y_shunt_pu)
print()

print("Y Buses")
circuit1.print_y_bus("positive")
circuit1.print_y_bus("negative")
circuit1.print_y_bus("zero")
circuit1.print_y_bus()
print()

print("Faults")
fault.calc_single_line_to_ground("bus3", 1, 0)
fault.calc_double_line_to_ground("bus3", 1, 0)
fault.calc_line_to_line("bus3",1, 0)
