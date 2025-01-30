from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from TransmissionLine import TransmissionLine as TransmissionLine
from Transformer import Transformer

#validate transformer
xfmr1 = Transformer("T1", "bus1", "bus2", 124, 8.5, 10)
print("name: ", xfmr1.name, "; should be T1")
print("bus1: ", xfmr1.bus1, "; should be bus1")
print("bus2: ", xfmr1.bus2, "; should be bus2")
print("power rating: ", xfmr1.power_rating, "; should be 124")
print("impedance percent: ", xfmr1.impedance_percent, "; should be 8.5")

xfmr1.calc_z()
xfmr1.calc_y()
print("z: ", xfmr1.z, "; should be ")
print("y: ", xfmr1.y, "; should be ")

xfmr1.calc_yprim()
xfmr1.print_yprim()

#**********CONDUCTOR VALIDATION******************
conductor1 = Conductor("Partridge", 0.642, 0.0217,0.385, 460)
print(conductor1.name, conductor1.diameter,conductor1.GMR, conductor1.resistance, conductor1.amp)
#*********BUS VALIDATION**************************
bus1 = (Bus("Bus 1", 20))
bus2 = Bus("Bus 2", 230)
print(bus1.name, bus1.base_kv, bus1.index)
print(bus2.name, bus2.base_kv, bus2.index)
#************BUNDLE VALIDATION**********************
bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(bundle1.name, bundle1.num_conductors,bundle1.spacing, bundle1.conductor.name)
print(bundle1.DSC, bundle1.DSL)
#*********GEOMETRY VALIDATION***************
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0,37, 0)
print(geometry1.name, geometry1.xa, geometry1.ya,geometry1.xb, geometry1.yb, geometry1.xc, geometry1.yc)
print(geometry1.Deq)
#*******************TRANSMISSION LINE VALIDATION************
line1 = TransmissionLine("Line 1", bus1, bus2,bundle1, geometry1, 10)
print(line1.name, line1.bus1.name, line1.bus2.name,line1.length)
print(line1.z_base, line1.y_base)
print(line1.Z, line1.B, line1.Y)
print(line1.y_matrix)