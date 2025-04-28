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
from Solution import Solution

settings = Settings()
circuit_3 = Circuit('Validation case 3',settings)

bus1= Bus("bus1", 13.8, "slack")
bus2= Bus("bus2", 345, "pq",)
bus3= Bus("bus3", 20, "pq")
bus4=Bus("bus4", 345, "pq")
bus5=Bus("bus5", 345, "pq")
bus6=Bus("bus6", 345, "pq")
bus7=Bus("bus7", 345, "pv")

circuit_3.add_bus(bus1)
circuit_3.add_bus(bus2)
circuit_3.add_bus(bus3)
circuit_3.add_bus(bus4)
circuit_3.add_bus(bus5)
circuit_3.add_bus(bus6)
circuit_3.add_bus(bus7)


T1=Transformer("T1", bus1, bus2, 350, 10, 10,'delta-y',1)
T2=Transformer("T2", bus3, bus4, 500, 12, 10,'delta-y',0)

circuit_3.add_transformer(T1)
circuit_3.add_transformer(T2)

conductor1 = Conductor("Cardinal",1.196,.0403,.1128,101)
circuit_3.add_conductor(conductor1)

geometry1 = Geometry("G1",0,0,28,4,28*2,0)
circuit_3.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)
circuit_3.add_bundle(bundle1)


tLine1 = TransmissionLine("tline1",bus2, bus5,bundle1,geometry1,100)
tLine2 = TransmissionLine("tline2",bus4, bus5,bundle1,geometry1,80)
tline3 = TransmissionLine("tline3",bus5, bus6,bundle1,geometry1,110)
tline4 = TransmissionLine("tline4",bus5, bus7,bundle1,geometry1,120)
tline5 = TransmissionLine('tline5',bus6, bus7,bundle1,geometry1,50)

circuit_3.add_transmission_line(tLine1)
circuit_3.add_transmission_line(tLine2)
circuit_3.add_transmission_line(tline3)
circuit_3.add_transmission_line(tline4)
circuit_3.add_transmission_line(tline5)

load3 = Load("load5",bus5,-200,-60,settings)
load6 = Load('load6',bus6,-245,-80,settings)
load7 = Load('load3',bus3,-180,-40,settings)
circuit_3.add_load(load3)
circuit_3.add_load(load6)
circuit_3.add_load(load7)

# ****************** Generator Initialization *************************
gen1 = Generator("Gen 1",bus1,0,100, .12,.14,.05,0,True,settings)
circuit_3.add_generator(gen1)
gen2 = Generator("Gen 2",bus7,0,300, .12,.14,.05,.01,True,settings)
circuit_3.add_generator(gen2)

#****************** Solution Object Initialization *************************
solution_3 = Solution(circuit_3)
circuit_3.calc_y_bus()

known =solution_3.calc_known_power()
print("Known power")
print(known)
mism = solution_3.calc_mismatch()
print("Mismatch")
print(mism)
jac = solution_3.calc_jacobian()
print("Jacobian")
print(jac)
guess = solution_3.calc_solutionRef()
print("Initial solution reference")
print(guess)
array,it = solution_3.calc_solution()
print("\n--- Solution Found ---")
print(f"Iterations: {it}")
print(f"{'V (pu)':>10} {'Angle (deg)':>15}")
print("-" * 26)
for row in array:
    print(f"{row[0]:>10.4f} {row[1]:>15.2f}")