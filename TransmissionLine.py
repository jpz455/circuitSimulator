from Bundle import Bundle as Bundle
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
from Settings import current_settings as current_settings
import numpy as np
import pandas as pd


class TransmissionLine:

    def __init__(self,name:str,bus1:Bus,bus2:Bus,bundle:Bundle,geometry:Geometry,length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.calculate_base_values()
        self.calculate_series_impedance()
        self.calculate_admittance()
        self.calculate_y_matrix()


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



    def calculate_y_matrix(self):
        prim_y = np.array([[self.Ytotal, -1 * self.Ypu], [-1 * self.Ypu, self.Ytotal]])
        self.matrix = {
            "y matrix": [prim_y[0,0], prim_y[0,1]],
            "": [prim_y[1,0], prim_y[1,1]]
        }


    def calculate_base_values(self):
        self.z_base = self.bus1.base_kv**2/current_settings.s_base
        self.y_base = 1/self.z_base

    def print_yprim(self):
        printout = pd.DataFrame(self.matrix)
        print(printout.to_string(index = False))