from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings
from TransmissionLine import TransmissionLine as TransmissionLine
from Fault import Fault
from Solution import Solution
from Load import Load
from Generator import Generator
from Transformer import Transformer
from Circuit import Circuit as Circuit

# ****************** Create circuit object **************************************
circuit = Circuit("Test Circuit", current_settings)

# ******************System bus initialization************************************
bus1= Bus("bus1", 20, "slack")
bus2= Bus("bus2", 230, "pq",)
bus3= Bus("bus3", 230, "pq")
bus4=Bus("bus4", 230, "pq")
bus5=Bus("bus5", 230, "pq")
bus6=Bus("bus6", 230, "pq")
bus7=Bus("bus7", 18, "pv")

circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)

# ****************** Transformer Initialization *************************

T1=Transformer("T1", bus1, bus2, 125, 8.5, 10,'delta-y',1)
T2=Transformer("T2", bus6, bus7, 200, 10.5, 12,'delta-y',0)

circuit.add_transformer(T1)
circuit.add_transformer(T2)

# ****************** Conductor Initialization *************************
conductor1 = Conductor("Partridge",.642,.0217,.385,460)
circuit.add_conductor(conductor1)

# ****************** Geometry/Bundle Initialization *************************
geometry1 = Geometry("G1",0,0,19.5,0,39,0)
circuit.add_geometry(geometry1)
bundle1 = Bundle('B1',2,1.5, conductor1)

# ****************** Transmission Line Initialization *************************
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

# ****************** Load Initialization *************************
load3 = Load("load3",bus3,-110,-50, current_settings)
circuit.add_load(load3)
load4 = Load("load4",bus4,-100,-70, current_settings)
circuit.add_load(load4)
load5 = Load("load5",bus5,-100,-65, current_settings)
circuit.add_load(load5)

# ****************** Generator Initialization *************************
gen1 = Generator("Gen 1",bus1,0,100, .12,.14,.05,0,True, current_settings)
circuit.add_generator(gen1)
gen2 = Generator("Gen 2",bus7,0,200, .12,.14,.05,.01,True, current_settings)
circuit.add_generator(gen2)

#****************** Solution Object Initialization *************************
solution = Solution(circuit)

#****************** Single Bus Fault Study *******************************
fault = Fault(circuit)
voltages, current = fault.calc_3_phase_bal("bus3")
print()
fault.print_fault_voltages()
print()
#****************** Power Flow ****************************************
solution.calc_jacobian()
solution.calc_known_power()
solution.calc_mismatch()
solution.calc_solutionRef()
solution.calc_solution()
#**************** Unbalanced Faults **********************************
print("Line to Line fault")
fault.calc_line_to_line("bus5",1, 0)
print("Double line to ground fault")
fault.calc_double_line_to_ground("bus5",1, 0)
print()
fault.calc_single_line_to_ground("bus5",1, 0)


