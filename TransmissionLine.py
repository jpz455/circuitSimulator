class TransmissionLine:

    def __init__(self,name:str,bus1:str,bus2:str,bundle:float,geometry:str,length:float):
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

def calculate_shunt_admittance(self):

def calculate_y_matrix(self):





