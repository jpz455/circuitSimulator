from Bus import Bus
from Settings import Settings
class Generator:
    def __init__(self,name:str,bus:Bus,voltage_setpoint:float,mw_setpoint:float, settings: Settings):
        self.name = name
        self.voltage_setpoint = voltage_setpoint #in pu
        self.mw_setpoint = mw_setpoint #in MW
        self.bus = bus
        self.settings: Settings = settings




