class Conductor:
    def __init__(self,name:str,diameter:float,GMR:float,resistance:float,amp:float):
        self.name = name
        self.diameter = diameter #outside diameter in inches
        self.GMR = GMR #at 60 Hz
        self.resistance = resistance
        self.amp = amp
        self.radius = self.diameter/24 #converting diameter to radius in inches


conductor1 = Conductor("Partridge", 0.642, 0.0217,0.385, 460)
print(conductor1.name, conductor1.diameter,conductor1.GMR, conductor1.resistance, conductor1.amp)