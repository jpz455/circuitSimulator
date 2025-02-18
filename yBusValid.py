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

bus1= Bus("bus1", 20)
bus2= Bus("bus2", 230)
bus3= Bus("bus3", 230)
bus4=Bus("bus4", 230)
bus5=Bus("bus5", 230)
bus6=Bus("bus6", 230)
bus7=Bus("bus7", 18)

# Add buses to circuit
circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

T1=Transformer("T1", bus1, bus2, 125, 8.5, 10)
T2= Transformer("T2", bus6, bus7, 200, 10.5, 12)

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

circuit.add_transmissionline(tLine1)
circuit.add_transmissionline(tLine2)
circuit.add_transmissionline(tLine3)
circuit.add_transmissionline(tLine4)
circuit.add_transmissionline(tLine5)
circuit.add_transmissionline(tLine6)

# Calculate Y-Bus Matrix
circuit.calc_ybus()

# Print the Y-Bus Matrix
circuit.print_ybus()
