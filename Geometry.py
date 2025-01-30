import numpy as np
class Geometry:
    def __init__(self,name:str,xa:float,ya:float,xb:float,yb:float,xc:float,yc:float):
        self.name = name
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb
        self.xc = xc
        self.yc = yc
        self.Deq = self.calculate_Deq()

    def calculate_Deq(self):
        #cube root(Dab*Dbc*Dca)
        self.Dab = np.sqrt((self.xa - self.xb) ** 2 + (self.ya - self.yb) ** 2)
        self.Dbc = np.sqrt((self.xb - self.xc) ** 2 + (self.yb - self.yc) ** 2)
        self.Dca = np.sqrt((self.xc - self.xa) ** 2 + (self.yc - self.ya) ** 2)
        self.Deq = np.power((self.Dab * self.Dbc * self.Dca),1/3)
        return self.Deq


geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0,37, 0)
print(geometry1.name, geometry1.xa, geometry1.ya,geometry1.xb, geometry1.yb, geometry1.xc, geometry1.yc)
print(geometry1.Deq)
