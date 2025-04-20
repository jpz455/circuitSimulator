from numpy.f2py.auxfuncs import throw_error


class Bus:
    numBus=0
    def __init__(self,name:str,base_kv:float, bus_type: str, v_pu: float = 1.0, delta: float = 0.0):
        self.name = name.strip().lower()
        self.base_kv = base_kv
        Bus.numBus += 1  # Increment the class variable
        self.index = Bus.numBus
        self.bus_type = bus_type
        self.v_pu = v_pu
        self.delta = delta

        self.set_bus_type() #validate bus_type


    def set_bus_type(self):
        if self.bus_type not in ["slack", "pq", "pv","Slack","PV","PQ"]:
            print("Bus type must be slack, pq or pv. Defaulting to PQ.")
            self.bus_type = "pq"

    def set_bus_V(self, bus_v: float):
        self.v_pu = bus_v

    def set_bus_delta(self, bus_angle: float):
        self.delta = bus_angle







