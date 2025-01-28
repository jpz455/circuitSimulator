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
