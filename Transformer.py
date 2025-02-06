import numpy as np
import pandas as pd
from typing import Dict
from Bus import Bus

from Settings import current_settings

class Transformer():
    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.z: float = (self.impedance_percent/100) * np.exp(1j * np.arctan(self.x_over_r_ratio))
        self.y: float = 1/self.z
        self.yprim: list[float] = []
        self.matrix: Dict[float, float] = {}
        self.calc_z()
        self.calc_r()
        self.calc_x()
        self.calc_b()
        self.calc_g()
        self.calc_y()

    def calc_z(self):
        self.z = (self.impedance_percent/100) * np.exp(1j * np.arctan(self.x_over_r_ratio))
    def calc_y(self):
        self.calc_z()
        self.y = 1/self.z
    def calc_x(self):
        self.x = np.imag(self.calc_z())
    def calc_r(self):
        self.r = np.real(self.calc_z())
    def calc_g(self):
        self.g = np.real(self.calc_z())
    def calc_b(self):
        self.b = np.imag(self.calc_z())
    def calc_yprim(self):
        self.calc_in_pu()
        ypp = self.ypu
        yps = -1 * self.ypu
        ysp = -1 * self.ypu
        yss = self.ypu
        self.yprim = [ypp, yps, ysp, yss]
        self.matrix = {
            "y matrix" : [ypp, yps],
            "" : [ysp, yss]
        }

    def calc_in_pu(self):
        self.v_base = 230
        self.z_base = self.v_base*self.v_base/current_settings.sbase
        self.y_base = 1/self.z_base
        self.xpu = self.x/self.z_base
        self.rpu = np.real(self.z)/self.z_base
        self.zpu = self.rpu + 1j*self.xpu
        self.gpu = np.real(self.y)/self.y_base
        self.bpu = self.b/self.y_base
        self.ypu = self.gpu + 1j*self.bpu


    def print_yprim(self):
        printout = pd.DataFrame(self.matrix)
        print(printout.to_string(index = False))
