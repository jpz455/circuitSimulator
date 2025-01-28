from Conductor import Conductor as Conductor

class Bundle:
    def __init__(self,name:str,num_conductors:float,spacing:float,conductor:Conductor):
        self.name = name
        self.num_conductors = num_conductors
        self.spacing = spacing
        self.conductor = conductor
    def calculate_DSC(self):
    def calculate_DSL(self):
