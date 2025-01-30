from setuptools import Require

import Bundle as bundle
import Bus as bus
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
print("ratio: ", xfmr1.x_over_r_ratio, "; should be 10")

xfmr1.calc_z()
xfmr1.calc_y()
print("z: ", xfmr1.z, "; should be ", 0.085*np.exp(1.47113*1j))
print("y: ", xfmr1.y, "; should be ", 1/(0.085*np.exp(1.47113*1j)))
print()


xfmr1.calc_yprim()
xfmr1.print_yprim()

