from Bundle import Bundle as Bundle
from Conductor import Conductor as Conductor
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from TransmissionLine import TransmissionLine as TransmissionLine
import numpy as np
from Transformer import Transformer

#************TRANSFORMER VALIDATION***********************#
xfmr1 = Transformer("T1", "bus1", "bus2", 124, 8.5, 10)
print("Transformer Validation")
print("name: ", xfmr1.name, "; should be T1")
print("bus1: ", xfmr1.bus1, "; should be bus1")
print("bus2: ", xfmr1.bus2, "; should be bus2")
print("power rating: ", xfmr1.power_rating, "; should be 124")
print("impedance percent: ", xfmr1.impedance_percent, "; should be 8.5")
print("ratio: ", xfmr1.x_over_r_ratio, "; should be 10")

xfmr1.calc_z()
xfmr1.calc_y()
print("z: ", xfmr1.z, "; should be ", 0.085*np.exp(1.47113*1j))
print("y: ", xfmr1.y, "; should be ", 1/(0.085*np.exp(1.47113*1j)))
print()

xfmr1.calc_yprim()
xfmr1.print_yprim()
print()
#**********CONDUCTOR VALIDATION******************
conductor1 = Conductor("Partridge", 0.642, 0.0217,0.385, 460)
print("name:", conductor1.name, ";should be Partridge");
print("diameter:", conductor1.diameter, ";should be 0.642")
print("GMR:", conductor1.GMR, ";should be 0.0217")
print("resistance:", conductor1.resistance, ";should be 0.385")
print("amperage:", conductor1.amp, ";should be 460")
print()
#*********BUS VALIDATION**************************
bus1 = (Bus("Bus 1", 20))
bus2 = Bus("Bus 2", 230)
print("Bus Validation")
print("bus1 name:", bus1.name, "; should be Bus 1")
print("bus1 base voltage:", bus1.base_kv, ";should be 20")
print("bus1 index:", bus1.index, "; should be 0")
print("bus2 name:", bus2.name, "; should be Bus 2")
print("bus 2 base voltage:", bus2.base_kv, ";should be 230")
print("bus 2 index: ", bus2.index, "; should be 1")
print()
#************BUNDLE VALIDATION**********************
bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(bundle1.name, bundle1.num_conductors,bundle1.spacing, bundle1.conductor.name)
print("Bundle Validation")
print("bundle1 name:", bundle1.name, "; should be Bundle 1")
print("bundle1 num conductors:", bundle1.num_conductors, "; should be 2")
print("bundle1 spacing:", bundle1.spacing, "; should be 1.5")
print("bundle1 DSC:", bundle1.DSC)
print("bundle1 DSL:", bundle1.DSL)
print()
#*********GEOMETRY VALIDATION***************
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0,37, 0)
print("Geometry Validation")
print("Geometry 1 name:", geometry1.name, "; should be Geometry 1")
print("Geometry 1 xa:", geometry1.xa, "; should be 0")
print("Geometry 1 ya:", geometry1.ya, "; should be 0")
print("Geometry 1 xb:", geometry1.xb, "; should be 18.5")
print("Geometry 1 yb:", geometry1.yb, "; should be 0")
print("Geometry 1 xc:", geometry1.xc, "; should be 37")
print("Geometry 1 yc:", geometry1.yc, "; should be 0")
print("Geometry 1 Deq:", geometry1.Deq)
print()
#*******************TRANSMISSION LINE VALIDATION************
line1 = TransmissionLine("Line 1", bus1, bus2,bundle1, geometry1, 10)
print("TransmissionLine Validation")
print("Line 1 name:", line1.name, "; should be Line 1")
print("Line 1 length:", line1.length, "; should be 10")
print("Line 1 Z:", line1.Z)
print("Line 1 Y:", line1.Y)
print("Line 1 B:", line1.B)
print("Y Matrix: ", line1.y_matrix)
print()