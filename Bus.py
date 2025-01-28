
class Bus:
    numBus=0
    def __init__(self,name:str,base_kv:float):
        self.name = name
        self.base_kv = base_kv
        Bus.numBus += 1  # Increment the class variable
        self.index = Bus.numBus











