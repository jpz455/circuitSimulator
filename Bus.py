
class Bus:
    numBus=0
    def __init__(self,name:str,base_kv:float):
        self.name = name
        self.base_kv = base_kv
        Bus.numBus += 1  # Increment the class variable
        self.index = Bus.numBus


bus1 = (Bus("Bus 1", 20))
bus2 = Bus("Bus 2", 230)
print(bus1.name, bus1.base_kv, bus1.index)
print(bus2.name, bus2.base_kv, bus2.index)







