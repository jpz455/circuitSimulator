#sets global variables for power base, frequency
class Settings:
    def __init__(self, f= 60, s_base = 100):
        self.f = f
        self.s_base = s_base

current_settings = Settings()