import numpy as np
import pandas as pd
from typing import Dict

class Transformer():
    def __init__(self, name: str, bus1: str, bus2: str, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.z: complex = self.impedance_percent * np.exp(1j * np.arctan(self.x_over_r_ratio))
        self.y: complex = 1/self.z
        self.g: float
        self.b: float
        self.r: float
        self.x: float
        self.yprim: list[float] = []
        self.matrix: Dict[float, float] = {}

    def calc_z(self):
        self.impedance_percent = self.impedance_percent * np.exp(1j * np.arctan(self.x_over_r_ratio))
    def calc_y(self):
        self.calc_z()
        self.y = 1/self.z
    def calc_x(self):
        np.imag(self.calc_z())
    def calc_r(self):
        np.real(self.calc_z())
    def calc_g(self):
        np.real(self.calc_z())
    def calc_b(self):
        np.imag(self.calc_z())
    def calc_yprim(self):
        ypp = self.y
        yps = -1 * self.y
        ysp = -1 * self.y
        yss = self.y
        self.yprim = [ypp, yps, ysp, yss]
        self.matrix = {
            "" : [ypp, yps],
            "" : [ysp, yss]
        }

    def print_yprim(self):
        printout = pd.DataFrame(self.matrix)
        print(printout.to_string(index = False))
