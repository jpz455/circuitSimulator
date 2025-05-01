import schemdraw as sd
import schemdraw.elements as elm
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from Circuit import Circuit
from Generator import Generator
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Load import Load
from Bus import Bus
import numpy as np

class GUI:
    def __init__(self, circuit: Circuit):
        self.circuit: Circuit = circuit #circuit
        self.gen_elms = circuit.generators # all generators
        self.load_elms = circuit.loads # all loads
        self.line_elms = circuit.transmission_lines # all lines
        self.trans_elms = circuit.transformers # all transformers
        self.bus_elms = circuit.buses # all buses
        self.staggered_lines = 0 # holds the number of lines that are more than 1 bus apart
        self.diagram = sd.Drawing()


