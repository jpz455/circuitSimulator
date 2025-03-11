
from Bundle import Bundle
from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from Settings import Settings
from Circuit import Circuit
import numpy as np
from Solution import Solution

#test case for power mismatch

# Initialize settings
settings = Settings()

# Create the circuit
circuit = Circuit("Power Flow Test Circuit", settings)

# Create and add buses
bus1= Bus("bus1", 20, "slack")
bus2= Bus("bus2", 230, "pq")
bus3= Bus("bus3", 18, "pq")

circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)

# Create and add transformer
T1=Transformer("T1", bus1, bus2, 125, 8.5, 10)
circuit.add_transformer(T1)

# Create & add conductor
conductor1 = Conductor("Partridge",.642,.0217,.385,460)
circuit.add_conductor(conductor1)

# Create geometry & bundle & add
geometry1 = Geometry("G1",0,0,19.5,0,39,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)

# Create & add transmission lines
tLine1 = TransmissionLine("tline1",bus1, bus2, bundle1, geometry1,10)
tLine2 = TransmissionLine("tline2",bus2, bus3, bundle1, geometry1,10)

# Calculate & print Y-Bus matrix
y_bus = circuit.calc_y_bus()
circuit.print_y_bus()

# Calculate power mismatch
buses = np.array([bus1, bus2, bus3])
v1 = bus1.v_pu*bus1.base_kv*np.exp(1j*bus1.delta)
v2 = bus2.v_pu*bus2.base_kv*np.exp(1j*bus2.delta)
v3 = bus3.v_pu*bus3.base_kv*np.exp(1j*bus3.delta)
voltages = np.array([v1, v2, v3])
solution = Solution(circuit)

print()
vector = solution.compute_power_mismatch(buses, y_bus, voltages)
print(vector)

