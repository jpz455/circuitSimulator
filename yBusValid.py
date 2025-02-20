from Bundle import Bundle
from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from Settings import Settings
from Circuit import Circuit
import numpy as np

# Initialize settings
settings = Settings()

# Create the circuit
circuit = Circuit("Power Flow Test Circuit", settings)

# Define buses

bus1= Bus("bus1", 20, "Slack")
bus2= Bus("bus2", 230, "PQ")
bus3= Bus("bus3", 230, "PQ")
bus4=Bus("bus4", 230, "PQ")
bus5=Bus("bus5", 230, "PQ")
bus6=Bus("bus6", 230, "PQ")
bus7=Bus("bus7", 18, "PQ")

# Add buses to circuit
circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

T1=Transformer("T1", bus1, bus2, 125, 8.5, 10)
T2=Transformer("T2", bus6, bus7, 200, 10.5, 12)

circuit.add_transformer(T1)
circuit.add_transformer(T2)

# Define conductor
conductor1 = Conductor("Partridge",.1013,.0217,.385,460)
circuit.add_conductor(conductor1)

# Define geometry
geometry1 = Geometry("G1",0,0,9.75,0,19.5,0)
circuit.add_geometry(geometry1)

bundle1 = Bundle('B1',2,1.5,conductor1)
# Define transmission lines

tLine1 = TransmissionLine("tline1",bus2, bus4,bundle1,geometry1,10)
tLine2 = TransmissionLine("tline2",bus2, bus3,bundle1,geometry1,25)
tLine3 = TransmissionLine("tline3",bus3, bus5,bundle1,geometry1,20)
tLine4 = TransmissionLine("tline4",bus4, bus6,bundle1,geometry1,20)
tLine5 = TransmissionLine("tline5",bus5, bus6,bundle1,geometry1,10)
tLine6 = TransmissionLine("tline6",bus4, bus5,bundle1,geometry1,35)

circuit.add_transmission_line(tLine1)
circuit.add_transmission_line(tLine2)
circuit.add_transmission_line(tLine3)
circuit.add_transmission_line(tLine4)
circuit.add_transmission_line(tLine5)
circuit.add_transmission_line(tLine6)

# Calculate Y-Bus Matrix
circuit.calc_y_bus()

# Print the Y-Bus Matrix
circuit.print_y_bus()

#print values for PowerWorld
print("xfmr1 r: ", T1.r_pu)
print("xfmr1 x: ", T1.x_pu)
print()

print("xfmr2 r: ", T2.r_pu)
print("xfmr2 x: ", T2.x_pu)
print()

print("tl1 r: ", tLine1.rpu)
print("tl1 x: ", tLine1.xpu)
print("tl1 b: ", np.imag(tLine1.y_shunt_pu))
print()

print("tl2 r: ", tLine2.rpu)
print("tl2 x: ", tLine2.xpu)
print("tl2 b: ", np.imag(tLine2.y_shunt_pu))
print()

print("tl3 r: ", tLine3.rpu)
print("tl3 x: ", tLine3.xpu)
print("tl3 b: ", np.imag(tLine3.y_shunt_pu))
print()

print("tl4 r: ", tLine4.rpu)
print("tl4 x: ", tLine4.xpu)
print("tl4 b: ", np.imag(tLine4.y_shunt_pu))
print()

print("tl5 r: ", tLine5.rpu)
print("tl5 x: ", tLine5.xpu)
print("tl5 b: ", np.imag(tLine5.y_shunt_pu))
print()

print("tl6 r: ", tLine6.rpu)
print("tl6 x: ", tLine6.xpu)
print("tl6 b: ", np.imag(tLine6.y_shunt_pu))
