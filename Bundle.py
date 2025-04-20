from Conductor import Conductor as Conductor
import numpy as np
class Bundle:
    def __init__(self, name: str, num_conductors, spacing: float, conductor: Conductor):


        try:
            num_conductors = int(num_conductors)
        except Exception:
            raise ValueError("Number of conductors must be convertible to an integer.")

        if num_conductors < 1:
            raise ValueError("Number of conductors must be ≥ 1.")

        if spacing <= 0:
            raise ValueError("Spacing must be a positive value.")

        self.name = name
        self.spacing = spacing
        self.num_conductors = num_conductors
        self.conductor = conductor

        # Adjust bundle resistance
        self.resistance = self.conductor.resistance / self.num_conductors

        # Calculate D_SL and D_SC
        self.DSL = self.calculate_DSL()
        self.DSC = self.calculate_DSC()


    def calculate_DSL(self):
        if self.num_conductors == 1:
            return self.conductor.GMR
        elif self.num_conductors == 2:
            return np.sqrt(self.conductor.GMR * self.spacing)
        elif self.num_conductors == 3:
            return (self.conductor.GMR * (self.spacing ** 2)) ** (1 / 3)
        elif self.num_conductors == 4:
            return 1.0941 * (self.conductor.GMR * (self.spacing ** 3)) ** (1 / 4)
        else:
            raise ValueError("Unexpected number of conductors: greater than 4.")

    def calculate_DSC(self):
        if self.num_conductors == 1:
            return self.conductor.radius
        elif self.num_conductors == 2:
            return np.sqrt(self.conductor.radius * self.spacing)
        elif self.num_conductors == 3:
            return (self.conductor.radius * (self.spacing ** 2)) ** (1 / 3)
        elif self.num_conductors == 4:
            return 1.0941 * (self.conductor.radius * (self.spacing ** 3)) ** (1 / 4)
        else:
            raise ValueError("Unexpected number of conductors: greater than 4.")

