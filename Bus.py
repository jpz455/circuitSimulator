from numpy.f2py.auxfuncs import throw_error


class Bus:
    numBus=0
    def __init__(self,name:str,base_kv:float, bus_type: str, v_pu: float = 1.0, delta: float = 0.0):
        self.name = name
        self.base_kv = base_kv
        Bus.numBus += 1  # Increment the class variable
        self.index = Bus.numBus
        self.bus_type = bus_type
        self.v_pu = v_pu
        self.delta = delta

        self.set_bus_type() #validate bus_type


    def set_bus_type(self):
        self.bus_type_check = self.bus_type.lower()
        if self.bus_type_check != "slack" or self.bus_type_check != "pq" or self.bus_type_check != "pv":
            throw_error("Bus type must be Slack or PQ or PV")







