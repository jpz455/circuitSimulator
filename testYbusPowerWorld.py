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
circuit = Circuit("simple circuit", settings)

# Define buses
bus2= Bus("bus2", 230)
bus3= Bus("bus3", 230)

# Add buses to circuit
circuit.add_bus(bus2)
circuit.add_bus(bus3)

# Define conductor
conductor1 = Conductor("Partridge",.1013,.0217,.385,460)
circuit.add_conductor(conductor1)

# Define geometry
geometry1 = Geometry("G1",0,0,9.75,0,19.5,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5,conductor1)

#Define line
tline = TransmissionLine("tline",bus2, bus3,bundle1,geometry1,10)

#add line
circuit.add_transmissionline(tline)

# Print the Y-Bus Matrix
circuit.calc_ybus()
circuit.print_ybus()

#print yprim
tline.calc_yprim()
tline.print_yprim()

print()

#print values for powerworld
print("tl1 r: ", tline.Rpu)
print("tl1 x: ", tline.Xpu)
print("tl1 b: ", tline.Yshuntpu)
print()

