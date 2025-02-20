import numpy as np
import pandas as pd
from typing import Dict
from Bus import Bus

from Settings import current_settings

class Transformer():
    def __init__(self, name: str, bus1: Bus, bus2:Bus, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio

        self.settings = current_settings


        self.z: float = (self.impedance_percent/100) * np.exp(1j * np.arctan(self.x_over_r_ratio))
        self.y: float = 1/self.z
        self.x: float = self.calc_x()
        self.r: float = self.calc_r()
        self.z_pu: float = self.z * (current_settings.s_base / self.power_rating)
        self.y_pu: float = 1 / self.z_pu
        self.r_pu: float = np.real(self.z_pu)
        self.x_pu: float = np.imag(self.z_pu)
        self.y_prim: np.array = self.calc_y_prim()
        self.matrix: Dict[float, float] = {}

    def calc_x(self):
        self.x = np.imag(self.z)
        return self.x
    def calc_r(self):
        self.r = np.real(self.z)
        return self.r
    def calc_y_prim(self):

        # Create the Y-prim matrix as a 2x2 matrix using the ypu values
        self.y_prim = np.array([[self.y_pu, -1 * self.y_pu],
                                [-1 * self.y_pu, self.y_pu]])

        # Convert the numpy array to a DataFrame
        self.y_prim = pd.DataFrame(self.y_prim, index=[self.bus1.name, self.bus2.name],
                                   columns=[self.bus1.name, self.bus2.name])

        # Create the matrix dictionary with entries from the DataFrame
        self.matrix = {
            "y matrix": [self.y_prim.iloc[0, 0], self.y_prim.iloc[0, 1]],  # Accessing first row values
            "": [self.y_prim.iloc[1, 0], self.y_prim.iloc[1, 1]]  # Accessing second row values
        }

        return self.y_prim

    def print_y_prim(self):
        print(self.y_prim)
