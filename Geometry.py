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
        self.Dab: float = np.sqrt((self.xa - self.xb) ** 2 + (self.ya - self.yb) ** 2)
        self.Dbc: float = np.sqrt((self.xb - self.xc) ** 2 + (self.yb - self.yc) ** 2)
        self.Dca: float = np.sqrt((self.xc - self.xa) ** 2 + (self.yc - self.ya) ** 2)
        self.Deq = self.calculate_Deq()

    def calculate_Deq(self):
        #cube root(Dab*Dbc*Dca)
        self.Deq = np.power((self.Dab * self.Dbc * self.Dca), 1/3)
        return self.Deq



