#sets global variables for power base, frequency
class Settings:
    def __init__(self, f= 60, s_base = 100):
        self._f = f
        self._s_base = s_base

    @property
    def f(self):
        return self._f

    @property
    def s_base(self):
        return self._s_base

current_settings = Settings()