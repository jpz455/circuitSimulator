import numpy as np
import pandas as pd
from typing import Dict
from Bus import Bus
from Settings import current_settings

class Transformer:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float,
                 impedance_percent: float, x_over_r_ratio: float,
                 connection_type: str, grounding_x: float = 0.0):

        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.connection_type = connection_type.lower()
        self.grounding_x = grounding_x
        self.settings = current_settings
        self.z_base1 = (self.bus1.base_kv ** 2) / current_settings.s_base
        self.z_base2 = (self.bus2.base_kv ** 2) / current_settings.s_base

        # Impedance and admittance in pu
        self.z = (self.impedance_percent / 100) * np.exp(1j * np.arctan(self.x_over_r_ratio))
        self.z_pu = self.z * (self.settings.s_base / self.power_rating)
        self.y_pu = 1 / self.z_pu
        self.r_pu = np.real(self.z_pu)
        self.x_pu = np.imag(self.z_pu)

        # Y matrices for different sequences
        self.y_prim_1 = self.calc_y_prim_pos_seq()
        self.y_prim_2 = self.calc_y_prim_neg_seq()
        self.y_prim_0 = self.calc_y_prim_zero_seq()

        self.matrix: Dict[str, complex] = {}

    def calc_y_prim_pos_seq(self):
        y = self.y_pu
        y_prim = np.array([[y, -y], [-y, y]])
        return pd.DataFrame(y_prim, index=[self.bus1.name, self.bus2.name],
                            columns=[self.bus1.name, self.bus2.name])

    def calc_y_prim_neg_seq(self):
        # Same as positive-sequence for symmetrical components
        return self.y_prim_1.copy()

    def calc_y_prim_zero_seq(self):
        y_prim_0 = np.zeros((2, 2), dtype=complex)
        z = self.z_pu

        if self.connection_type == "y-y":
            if self.grounding_x > 0:
                z_total = z + 2 * 3 * self.grounding_x
                y_total = 1 / z_total
                y_prim_0 = np.array([[y_total, -y_total], [-y_total, y_total]])

        elif self.connection_type == "y-delta":
            if self.grounding_x > 0:
                z_total = z + 3 * self.grounding_x
                y_total = 1 / z_total
                y_prim_0 = np.array([[y_total, 0], [0, 0]])

        elif self.connection_type == "delta-y":
            if self.grounding_x > 0:
                z_total = z + 3 * self.grounding_x
                y_total = 1 / z_total
                y_prim_0 = np.array([[0, 0], [0, y_total]])

        elif self.connection_type == "delta-delta":
            y_prim_0 = np.zeros((2, 2), dtype=complex)

        else:
            raise ValueError("Invalid connection type. Must be y-y, y-delta, delta-y, or delta-delta.")

        df = pd.DataFrame(y_prim_0, index=[self.bus1.name, self.bus2.name],
                          columns=[self.bus1.name, self.bus2.name])
        return df

    def print_y_prim(self):
        print(f"\n--- Transformer {self.name} Y-Prim Matrices ---")
        print("Positive Sequence (1):\n", self.y_prim_1)
        print("\nNegative Sequence (2):\n", self.y_prim_2)
        print("\nZero Sequence (0):\n", self.y_prim_0)
