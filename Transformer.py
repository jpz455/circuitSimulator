import numpy as np
import pandas as pd
from typing import Dict
from Bus import Bus
from Settings import current_settings

class Transformer():
    def __init__(self, name: str, bus1: Bus, bus2:Bus, power_rating: float, impedance_percent: float, x_over_r_ratio: float, connection_type: str = "y-y", grounding_x: float = 0):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio
        self.connection_type = connection_type
        self.grounding_x = grounding_x
        self.settings = current_settings
        self.z = (self.impedance_percent/100) * np.exp(1j * np.arctan(self.x_over_r_ratio))
        self.y = 1/self.z
        self.x = np.imag(self.z)
        self.r = np.real(self.z)
        self.z_pu = self.z * (current_settings.s_base / self.power_rating)
        self.y_pu = 1 / self.z_pu
        self.r_pu = np.real(self.z_pu)
        self.x_pu = np.imag(self.z_pu)
        self.y_prim_1 = self.calc_y_prim_1()
        self.y_prim_2 = self.calc_y_prim_2()
        self.y_prim_0 = self.calc_y_prim_0()
        self.matrix: Dict[str, complex] = {}

    def calc_y_prim_1(self):
            self.y_prim_1 = np.array([[self.y_pu, -1 * self.y_pu],
                                      [-1 * self.y_pu, self.y_pu]])
            # Convert the numpy array to a DataFrame
            self.y_prim_1 = pd.DataFrame(self.y_prim_1, index=[self.bus1.name, self.bus2.name],
                                         columns=[self.bus1.name, self.bus2.name])
            # Create the matrix dictionary with entries from the DataFrame
            self.matrix = {
                "y matrix": [self.y_prim_1.iloc[0, 0], self.y_prim_1.iloc[0, 1]],  # Accessing first row values
                "": [self.y_prim_1.iloc[1, 0], self.y_prim_1.iloc[1, 1]]  # Accessing second row values
            }
            return self.y_prim_1

    def print_y_prim(self, seq: int = 1):
        print(self.y_prim_1)

    def calc_y_prim_2(self):
        self.y_prim_2 = self.y_prim_1
        return self.y_prim_2

    def calc_y_prim_0(self):
        #get impedance/admittance
        z_ttl_pu = 3 * self.grounding_x + self.z_pu  # Zn and Z0 in series
        y_ttl_pu = 1 / z_ttl_pu  # convert to y

        #now determine based on connection type:
        if(self.connection_type == "y-y"):
            #everything is connected
            self.y_prim_0 = np.array([[y_ttl_pu, -1 * y_ttl_pu],
                                      [-1 * y_ttl_pu, y_ttl_pu]])

        elif((self.connection_type == "y-delta")):
            #bus 2 disconnected because delta
            z_ttl_pu = 3*self.grounding_x + self.z_pu
            y_ttl_pu = 1/z_ttl_pu
            self.y_prim_0 = np.array([[y_ttl_pu, 0],
                                      [0, 0]])

        elif((self.connection_type == "delta-y")):
            #bus 1 disconnected because delta
            z_ttl_pu = 3 * self.grounding_x + self.z_pu
            y_ttl_pu = 1 / z_ttl_pu
            self.y_prim_0 = np.array([[0, 0],
                                      [0, y_ttl_pu]])

        elif(self.connection_type == "delta-delta"):
            #everything disconnected
            self.y_prim_0= np.array([[0, 0],
                                     [0,0]])
        else:
            print("Invalid connection type. Must be y-y. y-delta, delta-y, or delta-delta.")

        # Convert the numpy array to a DataFrame
        self.y_prim_0 = pd.DataFrame(self.y_prim_0, index=[self.bus1.name, self.bus2.name],
                                         columns=[self.bus1.name, self.bus2.name])

        # Create the matrix dictionary with entries from the DataFrame
        self.matrix = {
        "y matrix": [self.y_prim_0.iloc[0, 0], self.y_prim_0.iloc[0, 1]],  # Accessing first row values
        "": [self.y_prim_0.iloc[1, 0], self.y_prim_0.iloc[1, 1]]  # Accessing second row values
        }
        return self.y_prim_0


