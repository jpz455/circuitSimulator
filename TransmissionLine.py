from Bundle import Bundle as Bundle
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings as current_settings
import numpy as np
import pandas as pd

class TransmissionLine:

    def __init__(self,name:str,bus1: str, bus2: str, bus_dict: dict,bundle:Bundle,geometry:Geometry,length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bus_dict = bus_dict 
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.calculate_base_values()
        self.calculate_series_impedance()
        self.calculate_admittance()
        self.calc_yprim()

    def get_bus(self, key: str):
        return self.bus_dict[key]

    def calculate_series_impedance(self):
        self.R = self.bundle.resistance
        #X = 2pif * (2e-7*ln(Deq/Dsl)*1609
        self.X = 2*np.pi*current_settings.f*2*10e-7*np.log(self.geometry.Deq/self.bundle.DSL)*1609
        self.Z = (self.R*self.length) + 1j * (self.X*self.length)
        self.Rpu = self.R/self.z_base
        self.Xpu = self.X/self.z_base
        self.Zpu = self.Z/self.z_base

    def calculate_admittance(self):
        #Y = 2pif*(2pi*eps*/ln(Deq/Dsc)*1609)
        self.B =1j*current_settings.f*((2*np.pi*np.power(8.85,-12))/(np.log(self.geometry.Deq/self.bundle.DSC))*1609)*self.length
        self.Y =1/self.Z

        #Y (series) = 1/Z (series)
        #Y (shunt) = G +jB

        self.Bpu = self.B/self.y_base
        self.Ypu = 1/self.Zpu
        self.Ytotal = self.Ypu +self.Bpu/2

    def calc_yprim(self):
        yprim_matrix = np.array([[self.Ytotal, -1 * self.Ypu], [-1 * self.Ypu, self.Ytotal]])
        self.yprim = {
            "y matrix": [yprim_matrix[0,0], yprim_matrix[0,1]],
            "": [yprim_matrix[1,0], yprim_matrix[1,1]]
        }
        # Creating a Pandas DataFrame with bus names as labels
        self.y_matrix_df = pd.DataFrame(yprim_matrix,index=[self.bus1, self.bus2],columns=[self.bus1, self.bus2])


    def calculate_base_values(self):
        bus1 = self.get_bus(self.bus1)  # Get Bus object dynamically
        self.z_base = (bus1.base_kv ** 2) / current_settings.s_base
        self.y_base = 1 / self.z_base

    def print_yprim(self):
        printout = pd.DataFrame(self.yprim)
        printout2 = pd.DataFrame(self.y_matrix_df)
        print(printout.to_string(index = False))
        print(printout2.to_string())



