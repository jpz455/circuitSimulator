from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings
from TransmissionLine import TransmissionLine as TransmissionLine
from Solution import Solution
from Load import Load
from Generator import Generator
from Transformer import Transformer
from Circuit import Circuit as Circuit

# ****************** Create circuit object **************************************
circuit = Circuit("Simple Circuit", current_settings)

# ******************System bus initialization************************************
bus1= Bus("bus1", 100, "slack")
bus2= Bus("bus2", 200, "pq")
bus3= Bus("bus3", 200, "pq")
bus4= Bus("bus4", 300, "pq")
bus5= Bus("bus5", 300, "pq")
bus6= Bus("bus6", 300, "pq")
bus7= Bus("bus7", 300, "pv")

circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

# ****************** Transformer Initialization *************************
T1=Transformer("T1", bus1, bus2, 100, 10, 10,'delta-y',1)
T2=Transformer("T2", bus3, bus4, 100, 10, 10,'delta-y',1)
circuit.add_transformer(T1)
circuit.add_transformer(T2)
#print to input into PowerWorld for validation
print(T1.r_pu, T1.x_pu)

# ****************** Conductor Initialization *************************
conductor1 = Conductor("Partridge",.642,.0217,.385,460)
circuit.add_conductor(conductor1)

# ****************** Geometry/Bundle Initialization *************************
geometry1 = Geometry("G1",0,0,19.5,0,39,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)

# ****************** Transmission Line Initialization *************************
tLine1 = TransmissionLine("tline1",bus2, bus3,bundle1,geometry1,20)
tLine2 = TransmissionLine("tLine2", bus4, bus5,bundle1,geometry1,20)
tLine3 = TransmissionLine("tLine3", bus5, bus6,bundle1,geometry1,20)
tLine4 = TransmissionLine("tLine4", bus6, bus7,bundle1,geometry1,20)

circuit.add_transmission_line(tLine1)
circuit.add_transmission_line(tLine2)
circuit.add_transmission_line(tLine3)
circuit.add_transmission_line(tLine4)

print(tLine1.r_pu, tLine1.x_pu, tLine1.y_shunt_pu)

# ****************** Load Initialization *************************
load1 = Load("load1",bus3,-100,-20, current_settings)
load2 = Load("load2",bus4,-200,-40, current_settings)
load3 = Load("load3",bus5,-250,-70, current_settings)

circuit.add_load(load1)
circuit.add_load(load2)
circuit.add_load(load3)

# ****************** Generator Initialization *************************
gen1 = Generator("Gen",bus1,0,100, .12,.14,.05,0,True, current_settings)
circuit.add_generator(gen1)
gen2 = Generator("Gen2", bus7, 300, 100, .12, .14, .05, 0, True, current_settings)
circuit.add_generator(gen2)
#****************** Solution  *************************
solution = Solution(circuit)
circuit.calc_y_bus_zero()
circuit.calc_y_bus_positive()
circuit.calc_y_bus_no_gen()
circuit.calc_y_bus_negative()
circuit.print_y_bus()

solution.calc_jacobian()
solution.calc_known_power()
solution.calc_mismatch()
solution.calc_solutionRef()
solution.calc_solution()



