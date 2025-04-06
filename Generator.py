from Bus import Bus
from Settings import Settings, current_settings


class Generator:
    def __init__(self,name:str,bus:Bus,voltage_setpoint:float,mw_setpoint:float, settings: Settings, base: float = 100):
        self.name = name
        self.voltage_setpoint = voltage_setpoint #in pu
        self.mw_setpoint = mw_setpoint #in MW
        self.bus = bus
        self.settings: Settings = settings
        self.subtransient_x = 0
        self.base = 100

    def set_subtransient_x(self, subtransient_x: float):
        self.subtransient_x = subtransient_x * (current_settings.s_base/self.base)







