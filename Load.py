from Settings import Settings
from Bus import Bus

class Load:
    def __init__(self,name:str,bus:Bus,real_pwr:float,reactive_pwr:float,settings:Settings):
        self.name = name
        self.bus = bus
        self.settings: Settings = settings
        self.reactive_pwr = reactive_pwr
        self.real_pwr = real_pwr


