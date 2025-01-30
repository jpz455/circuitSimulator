from Bundle import Bundle as Bundle
from Geometry import Geometry as Geometry
import numpy as np

class TransmissionLine:

    def __init__(self,name:str,bus1:str,bus2:str,bundle:Bundle,geometry:Geometry,length:float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        self.series_impedance = self.calculate_series_impedance()
        self.shunt_admittance = self.calculate_shunt_admittance()
        self.y_admittance_matrix = self.calculate_y_matrix()


    def calculate_series_impedance(self):
        resistance_per_mile = self.bundle.resistance 
        #X = 2pif * (2e-7*ln(Deq/Dsl)*1609
        reactance_per_mile = 2*np.pi*60*2*np.power(10,-7)*np.log(self.geometry.Deq/self.bundle.DSL)*1609
        series_impedance = (resistance_per_mile*self.length) + 1j * (reactance_per_mile*self.length)
        return series_impedance

    def calculate_shunt_admittance(self):
        #Y = 2pif*(2pi*eps*/ln(Deq/Dsc)*1609)
        admittance_per_mile = 2*np.pi*60*((2*np.pi*np.power(8.85,-12))/(np.log(self.geometry.Deq/self.bundle.DSC))*1609)
        series_admittance = 1j*admittance_per_mile*self.length
        return series_admittance

    def calculate_y_matrix(self):



