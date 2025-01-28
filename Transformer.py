import numpy as np

class Transformer():
    def __init__(self, name: str, bus1: str, bus2: str, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.z = self.calc_z()
        self.y = self.calc_y()

    def calc_z(self):
        self.impedance_percent = self.impedance_percent * np.exp(1j * np.arctan(self.x_over_r_ratio))
    def calc_y(self):
        self.calc_z()
        self.admittance = 1/self.impedance
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
        yps = self.