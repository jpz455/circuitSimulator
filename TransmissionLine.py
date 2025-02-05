from Bundle import Bundle as Bundle
from Bus import Bus as Bus
from Geometry import Geometry as Geometry
import numpy as np
import pandas as pd

from Conductor import Conductor


class TransmissionLine:

    def __init__(self,name:str,bus1:Bus,bus2:Bus,bundle:Bundle,geometry:Geometry,length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.calculate_series_impedance()
        self.calculate_admittance()
        self.calculate_y_matrix()
        self.calculate_base_values()

    def calculate_series_impedance(self):
        self.R = self.bundle.resistance
        #X = 2pif * (2e-7*ln(Deq/Dsl)*1609
        self.X = 2*np.pi*60*2*10e-7*np.log(self.geometry.Deq/self.bundle.DSL)*1609
        self.Z = (self.R*self.length) + 1j * (self.X*self.length)


    def calculate_admittance(self):
        #Y = 2pif*(2pi*eps*/ln(Deq/Dsc)*1609)
        self.B =1j* 2*np.pi*60*((2*np.pi*np.power(8.85,-12))/(np.log(self.geometry.Deq/self.bundle.DSC))*1609)*self.length
        self.Y =1/self.Z

    def calculate_y_matrix(self):
        y_prim = np.zeros((2,2),dtype=complex)
        y_prim[0,0] = y_prim[1,1] = self.Y + self.B /2
        y_prim[0,1] = y_prim[1,0] = -self.Y
        self.y_matrix = y_prim
        self.matrix = {
            "y matrix": [y_prim[0,0], y_prim[0,1]],
            "": [y_prim[1,0], y_prim[1,1]]
        }


    def calculate_base_values(self):
        self.z_base = self.bus1.base_kv**2/100e6   #using 100 MVA as default value for now
        self.y_base = 1/self.z_base

    def print_yprim(self):
        printout = pd.DataFrame(self.matrix)
        print(printout.to_string(index = False))


