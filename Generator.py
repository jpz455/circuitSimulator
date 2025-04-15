import numpy as np
import pandas as pd
from Bus import Bus
from Settings import Settings

class Generator:
    def __init__(self, name: str, bus: Bus, voltage_setpoint: float, mw_setpoint: float,x1: float, x2: float, x0: float, grounding_x: float ,grounded: bool , settings: Settings ):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint  # in pu
        self.mw_setpoint = mw_setpoint  # in MW
        self.x1 = x1
        self.x2 = x2
        self.x0 = x0
        self.settings = settings
        self.grounded = grounded
        self.grounding_x = grounding_x if grounded else None


        # Calculate per-unit admittances (Y = 1 / jX)
        self.y1 = 1 / (1j * self.x1)
        self.y2 = 1 / (1j * self.x2)
        self.y0 :complex


        if grounded and self.grounding_x > 0:
            z0_total = 1j * self.x0 + 3 * self.grounding_x  # 3x grounding impedance
        elif grounded:
            z0_total = 1j * self.x0  # solidly grounded
        else:
            z0_total = np.inf  # ungrounded -> open circuit for zero-sequence

        self.y0 = 0.0 if np.isinf(z0_total) else 1 / z0_total

        # Create 1x1 Y matrices since generator is connected to one bus
        self.y_prim_1 = pd.DataFrame([[self.y1]], index=[self.bus.name], columns=[self.bus.name])
        self.y_prim_2 = pd.DataFrame([[self.y2]], index=[self.bus.name], columns=[self.bus.name])
        self.y_prim_0 = pd.DataFrame([[self.y0]], index=[self.bus.name], columns=[self.bus.name])

    def print_y_prim(self, seq: int = 3):
       for seq in range(seq):
            if seq == 1:
                print(f"Generator {self.name} - Y Prim: Positive Sequence")
                print(self.y_prim_1)
            elif seq == 2:
                print(f"Generator {self.name} - Y Prim: Negative Sequence")
                print(self.y_prim_2)
            elif seq == 0:
                print(f"Generator {self.name} - Y Prim: Zero Sequence")
                print(self.y_prim_0)
            else:
                raise ValueError("Sequence must be 0, 1, or 2.")
