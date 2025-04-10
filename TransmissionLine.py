from Bundle import Bundle as Bundle
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings as current_settings
import numpy as np
import pandas as pd

class TransmissionLine:

    def __init__(self,name:str,bus1:Bus, bus2:Bus,bundle:Bundle,geometry:Geometry,length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length

        self.z_base = (self.bus1.base_kv ** 2) / current_settings.s_base
        self.y_base = 1 / self.z_base


        self.r = self.bundle.resistance * self.length
        # X = 2pif * (2e-7*ln(Deq/Dsl)*1609
        self.x = 2 * np.pi * current_settings.f * 2e-7 * np.log(self.geometry.Deq / self.bundle.DSL) * 1609 * self.length
        self.z = self.r + 1j * (self.x)
        self.r_pu: float = self.r / self.z_base
        self.x_pu: float = self.x / self.z_base
        self.z_pu: float = self.z / self.z_base



        # Y = 2pif*(2pi*eps*/ln(Deq/Dsc)*1609)
        # Y (shunt) = G +jB
        self.y_shunt =  1j * 2 * np.pi * current_settings.f * (2 * np.pi * 8.854e-12 / (np.log(self.geometry.Deq / self.bundle.DSC)) * 1609) * self.length
        # Y (series) = 1/Z (series)
        self.y_series =  1 / self.z
        self.y_series_pu = 1 / self.z_pu
        self.y_shunt_pu = self.y_shunt / self.y_base

        self.matrix: {}
        self.y_prim = self.calc_y_prim()
        self.y_prim_positive = None
        self.y_prim_negative = None
        self.y_prim_zero = None
        self.calc_y_prim_seq()



    def calc_y_prim(self):
        # Ensure that self.y_series_pu and self.y_shunt_pu are calculated before this step
        # The y_prim matrix is created based on these values
        # Create the Y-prim matrix as a 2x2 matrix using the y_series values
        # Create the Y-prim matrix as a 2x2 matrix using the y_series values
        self.y_prim = np.array([[self.y_series_pu + 0.5 * self.y_shunt_pu, -1 * self.y_series_pu],
                                [-1 * self.y_series_pu, self.y_series_pu + 0.5 * self.y_shunt_pu]])

        self.y_prim = pd.DataFrame(self.y_prim, index=[self.bus1.name, self.bus2.name],
                                   columns=[self.bus1.name, self.bus2.name])


        # Create the matrix dictionary with entries from the DataFrame
        self.matrix = {
            "y matrix": [self.y_prim.iloc[0, 0], self.y_prim.iloc[0, 1]],  # Accessing first row values
            "": [self.y_prim.iloc[1, 0], self.y_prim.iloc[1, 1]]  # Accessing second row values
        }

        return self.y_prim

    def calc_y_prim_seq(self):
        R_pu = self.r_pu
        X_pu = self.x_pu
        B_pu = self.y_shunt_pu.imag

        # Estimated sequence impedances and admittances
        Z0_pu = 2.5 * R_pu + 1j * X_pu
        Z1_pu = Z2_pu = R_pu + 1j * X_pu

        Y0_pu = 1 / Z0_pu
        Y1_pu = 1 / Z1_pu
        Y2_pu = 1 / Z2_pu

        Y_shunt_seq = 1j * B_pu

        def make_y_prim(y_val):
            return pd.DataFrame(
                np.array([
                    [y_val + 0.5 * Y_shunt_seq, -y_val],
                    [-y_val, y_val + 0.5 * Y_shunt_seq]
                ]),
                index=[self.bus1.name, self.bus2.name],
                columns=[self.bus1.name, self.bus2.name]
            )

        self.y_prim_positive = make_y_prim(Y1_pu)
        self.y_prim_negative = make_y_prim(Y2_pu)
        self.y_prim_zero = make_y_prim(Y0_pu)

    def print_y_prim(self):
        printout = pd.DataFrame(self.matrix)
        print(printout.to_string(index = False))




