#printing out the values I need for powerworld

import numpy as np
from Transformer import Transformer as xfmr, Transformer
from TransmissionLine import TransmissionLine as tl
from Circuit import Circuit as c
from Bus import Bus as bus
from Bundle import Bundle as bundle
from Conductor import Conductor as cond
from Geometry import Geometry as geom
from Settings import current_settings

#buses
bus1 = bus("Bus1", 20)
bus2 = bus("Bus2", 230)
bus3 = bus('Bus3', 230)
bus4 = bus("Bus4", 230)
bus5 = bus("Bus5", 230)
bus6 = bus("Bus6", 230)
bus7 = bus("Bus7", 18)

#transformers
xfmr1 = xfmr("Transformer1", bus1, bus2, 125, 8.5, 10)
xfmr2 = xfmr("Transformer2", bus6, bus7, 200, 10.5, 12)

#transmission lines
geom1 = geom('geom1',0,0,19.5,0,9.75, 7.75) #i think this is right based on line diagram?
cond1 = cond('cond1',.642/12,.0217,.385,460) #from ascr sheet, partridge
bundle1 = bundle('bundle1',3,1.5, cond1) #from diagram

tl1 = tl('TL1',bus2,bus4,bundle1,geom1,10)
tl2= tl('TL2',bus2,bus3,bundle1,geom1,25)
tl3 = tl('TL3',bus3,bus5,bundle1,geom1,20)
tl4 = tl('TL4',bus4,bus5,bundle1,geom1,20)
tl5 = tl('TL5',bus5,bus6,bundle1,geom1,10)
tl6 = tl('TL6',bus4,bus5,bundle1,geom1,35)

#circuit
circuit = c("circuit", current_settings)
#add buses
circuit.add_bus(bus1)
circuit.add_bus(bus2)
circuit.add_bus(bus3)
circuit.add_bus(bus4)
circuit.add_bus(bus5)
circuit.add_bus(bus6)
circuit.add_bus(bus7)
#add transformers
circuit.add_transformer(xfmr1)
circuit.add_transformer(xfmr2)
#add lines
circuit.add_transmissionline(tl1)
circuit.add_transmissionline(tl2)
circuit.add_transmissionline(tl3)
circuit.add_transmissionline(tl4)
circuit.add_transmissionline(tl5)
circuit.add_transmissionline(tl6)

#now get values for powerworld:
print("xfmr1 r: ", xfmr1.rpu)
print("xfmr1 x: ", xfmr1.xpu)
print()

print("xfmr2 r: ", xfmr2.rpu)
print("xfmr2 x: ", xfmr2.xpu)
print()

print("tl1 r: ", tl1.Rpu)
print("tl1 x: ", tl1.Xpu)
print("tl1 b: ", np.imag(tl1.Yshuntpu))
print()

print("tl2 r: ", tl2.Rpu)
print("tl2 x: ", tl2.Xpu)
print("tl2 b: ", np.imag(tl2.Yshuntpu))
print()

print("tl3 r: ", tl3.Rpu)
print("tl3 x: ", tl3.Xpu)
print("tl3 b: ", np.imag(tl3.Yshuntpu))
print()

print("tl4 r: ", tl4.Rpu)
print("tl4 x: ", tl4.Xpu)
print("tl4 b: ", np.imag(tl4.Yshuntpu))
print()

print("tl5 r: ", tl5.Rpu)
print("tl5 x: ", tl5.Xpu)
print("tl5 b: ", np.imag(tl5.Yshuntpu))
print()

print("tl6 r: ", tl6.Rpu)
print("tl6 x: ", tl6.Xpu)
print("tl6 b: ", np.imag(tl6.Yshuntpu))

#check y buses

print()
xfmr1.calc_yprim()
xfmr1.print_yprim()
print()
xfmr2.calc_yprim()
xfmr2.print_yprim()
print()
circuit.calc_ybus()
circuit.print_ybus()

