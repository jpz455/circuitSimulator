from Bus import Bus as Bus

class Generator:
    def __init__(self,name:str,bus:Bus,voltage_setpoint:float,mw_setpoint:float):
        self.name = name
        self.voltage_setpoint = voltage_setpoint #in pu
        self.mw_setpoint = mw_setpoint #in MW
        self.bus = bus



