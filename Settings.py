#sets global variables for power base, frequency
class Settings:
    def __init__(self, f= 60, sbase = 100):
        self.f = f
        self.sbase = sbase

current_settings = Settings()