from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import Settings
from TransmissionLine import TransmissionLine as TransmissionLine
import numpy as np
from Transformer import Transformer
from Circuit import Circuit as Circuit


# Initialize settings
settings = Settings()

# Create the circuit
circuit = Circuit("Basic Power Line Circuit", settings)

# Define buses
bus1= Bus("bus1", 230, "Slack")
bus2= Bus("bus2", 230, "PQ")

# Add buses to circuit
circuit.add_bus(bus1)
circuit.add_bus(bus2)

# Define conductor
conductor1 = Conductor("Partridge",.1013,.0217,.385,460)
circuit.add_conductor(conductor1)

# Define geometry
geometry1 = Geometry("G1",0,0,9.75,0,19.5,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5,conductor1)

# Define transmission line
tLine1 = TransmissionLine("tline1",bus1, bus2, bundle1, geometry1,10)

# add transmission line
circuit.add_transmission_line(tLine1)

# Calculate Y-Bus Matrix
circuit.calc_y_bus()

# Print the Y-Bus Matrix
circuit.print_y_bus()

#print values for PowerWorld
print()
print("tl1 r: ", tLine1.r_pu)
print("tl1 x: ", tLine1.x_pu)
print("tl1 b: ", np.imag(tLine1.y_shunt_pu))
print()
