from Bundle import Bundle
from Bus import Bus
from Transformer import Transformer
from Geometry import Geometry
from Conductor import Conductor
from TransmissionLine import TransmissionLine
from Settings import Settings
from Circuit import Circuit
from Load import Load
from Generator import Generator
import numpy as np
from Solution import Solution

#set up settings
settings = Settings()

#set up circuit
circuit = Circuit("circuit", settings)

#set up buses
bus1= Bus("bus1", 20, "slack")
bus2= Bus("bus2", 230, "pq",)
bus3= Bus("bus3", 230, "pq")
bus4=Bus("bus4", 230, "pq")
bus5=Bus("bus5", 230, "pq")
bus6=Bus("bus6", 230, "pq")
bus7=Bus("bus7", 18, "pv")
bus8=Bus("bus8", 18, "pq")
bus9=Bus("bus9", 18, "pq")
bus10=Bus("bus10", 18, "pq")

circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

#set up transformers
T1=Transformer("T1", bus1, bus2, 125, 8.5, 10)
T2=Transformer("T2", bus6, bus7, 200, 10.5, 12)

circuit.add_transformer(T1)
circuit.add_transformer(T2)

# set up conductors
conductor1 = Conductor("Partridge",.642,.0217,.385,460)
circuit.add_conductor(conductor1)

# set up geometry and bundle
geometry1 = Geometry("G1",0,0,19.5,0,39,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)

# set up transmission lines

tLine1 = TransmissionLine("tline1",bus2, bus4,bundle1,geometry1,10)
tLine2 = TransmissionLine("tline2",bus2, bus3,bundle1,geometry1,25)
tLine3 = TransmissionLine("tline3",bus3, bus5,bundle1,geometry1,20)
tLine4 = TransmissionLine("tline4",bus4, bus6,bundle1,geometry1,20)
tLine5 = TransmissionLine("tline5",bus5, bus6,bundle1,geometry1,10)
tLine6 = TransmissionLine("tline6",bus4, bus5,bundle1,geometry1,35)
tLine7 = TransmissionLine("tline7",bus5, bus6,bundle1,geometry1,20)
tLine8 = TransmissionLine("tline8",bus5, bus6,bundle1,geometry1,20)

circuit.add_transmission_line(tLine1)
circuit.add_transmission_line(tLine2)
circuit.add_transmission_line(tLine3)
circuit.add_transmission_line(tLine4)
circuit.add_transmission_line(tLine5)
circuit.add_transmission_line(tLine6)

