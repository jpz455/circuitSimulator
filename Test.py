from setuptools import Require

import Bundle as bundle
import Bus as bus
import TransmissionLine as line
import Transformer as xfmr
import numpy as np

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

