from Bundle import Bundle
from Bus import Bus
from Geometry import Geometry
from Settings import current_settings
import numpy as np
import pandas as pd

class TransmissionLine:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle: Bundle, geometry: Geometry, length: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length

        self.z_base = (self.bus1.base_kv ** 2) / current_settings.s_base
        self.y_base = 1 / self.z_base

        self._calculate_impedance()
        self._calculate_admittance()
        self.y_prim = self._calc_y_prim()
        self.y_prim_positive = None
        self.y_prim_negative = None
        self.y_prim_zero = None
        self._calc_sequence_admittance()

    def _calculate_impedance(self):
        self.r = self.bundle.resistance * self.length
        self.x = 2 * np.pi * current_settings.f * 2e-7 * np.log(self.geometry.Deq / self.bundle.DSL) * 1609 * self.length
        self.z = self.r + 1j * self.x

        self.r_pu = self.r / self.z_base
        self.x_pu = self.x / self.z_base
        self.z_pu = self.z / self.z_base

    def _calculate_admittance(self):
        eps = 8.854e-12
        self.y_shunt = 1j * 2 * np.pi * current_settings.f * (2 * np.pi * eps / np.log(self.geometry.Deq / self.bundle.DSC)) * 1609 * self.length
        self.y_shunt_pu = self.y_shunt / self.y_base
        self.y_series = 1 / self.z
        self.y_series_pu = 1 / self.z_pu

    def _calc_y_prim(self):
        y11 = self.y_series_pu + 0.5 * self.y_shunt_pu
        y12 = -self.y_series_pu
        matrix = np.array([[y11, y12], [y12, y11]])
        return pd.DataFrame(matrix, index=[self.bus1.name, self.bus2.name], columns=[self.bus1.name, self.bus2.name])

    def _calc_sequence_admittance(self):
        # Zero-sequence impedance typically uses a multiplier of around 2.5 to 3 times the line impedance
        Z0_pu = 2.5 * (self.r_pu + 1j * self.x_pu)
        Z1_pu = Z2_pu = self.r_pu + 1j * self.x_pu

        Y0_pu = 1 / Z0_pu
        Y1_pu = 1 / Z1_pu
        Y2_pu = 1 / Z2_pu
        Y_shunt_seq = 1j * self.y_shunt_pu.imag

        self.y_prim_positive = self._make_y_prim(Y1_pu, Y_shunt_seq)
        self.y_prim_negative = self._make_y_prim(Y2_pu, Y_shunt_seq)
        self.y_prim_zero = self._make_y_prim(Y0_pu, Y_shunt_seq)

    def _make_y_prim(self, y_series_pu, y_shunt_seq):
        y11 = y_series_pu + 0.5 * y_shunt_seq
        y12 = -y_series_pu
        return pd.DataFrame(
            np.array([[y11, y12], [y12, y11]]),
            index=[self.bus1.name, self.bus2.name],
            columns=[self.bus1.name, self.bus2.name]
        )

    def print_y_prim(self):
        print("Positive Sequence Y-Prim:\n", self.y_prim_positive)
        print("\nNegative Sequence Y-Prim:\n", self.y_prim_negative)
        print("\nZero Sequence Y-Prim:\n", self.y_prim_zero)
