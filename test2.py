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



# ****************** Initialization settings for system *************************
settings = Settings()

# ****************** Create circuit object **************************************
circuit2 = Circuit("Power Flow Test Circuit 2", settings)

# ******************System bus initialization************************************
bus_1= Bus("bus1", 20, "slack")
bus_2= Bus("bus2", 230, "pq",)
bus_3=Bus("bus3", 230, "pq")
bus_4=Bus("bus4", 230, "pq")
bus_5=Bus("bus5", 18, "pv")


circuit2.add_bus(bus_1)
circuit2.add_bus(bus_2)
circuit2.add_bus(bus_3)
circuit2.add_bus(bus_4)
circuit2.add_bus(bus_5)


# ****************** Transformer Initialization *************************

T12=Transformer("T1", bus_1, bus_2, 125, 8.5, 10,'delta-y',1)
T22=Transformer("T2", bus_4, bus_5, 200, 10.5, 12,'delta-y',0)

circuit2.add_transformer(T12)
circuit2.add_transformer(T22)

# ****************** Conductor Initialization *************************
conductor12 = Conductor("Partridge",.642,.0217,.385,460)
circuit2.add_conductor(conductor12)

# ****************** Geometry/Bundle Initialization *************************
geometry12 = Geometry("G1",0,0,19.5,0,39,0)
circuit2.add_geometry(geometry12)
bundle12 = Bundle('B1',2,1.5, conductor12)
circuit2.add_bundle(bundle12)
# ****************** Transmission Line Initialization *************************
tLine1 = TransmissionLine("tline1",bus_2, bus_4,bundle12,geometry12,10)
tLine2 = TransmissionLine("tline2",bus_2, bus_3,bundle12,geometry12,25)
tline3 = TransmissionLine("tline3",bus_3, bus_4,bundle12,geometry12,20)



circuit2.add_transmission_line(tLine1)
circuit2.add_transmission_line(tLine2)
circuit2.add_transmission_line(tline3)


# ****************** Load Initialization *************************

load32 = Load("load3",bus_3,-100,-70,settings)
circuit2.add_load(load32)


# ****************** Generator Initialization *************************
gen12 = Generator("Gen 1",bus_1,0,100, .12,.14,.05,0,True,settings)
circuit2.add_generator(gen12)
gen22 = Generator("Gen 2",bus_5,0,200, .12,.14,.05,.01,True,settings)
circuit2.add_generator(gen22)

#****************** Solution Object Initialization *************************
solution2 = Solution(circuit2)

#****************** Y Buses *******************************************

circuit2.calc_y_bus()
circuit2.print_y_bus()
known =solution2.calc_known_power()
print("Known power")
print(known)
mism = solution2.calc_mismatch()
print("Mismatch")
print(mism)
jac = solution2.calc_jacobian()
print("Jacobian")
print(jac)
guess = solution2.calc_solutionRef()
print("Initial solution reference")
print(guess)
print("solution")
print(solution2.calc_solution())
#****************** Power Flow ****************************************



#****************** Y Buses *******************************************

