import schemdraw as sd
import schemdraw.elements as elm
from Circuit import Circuit
import numpy as np

class GUI:
    def __init__(self, circuit: Circuit):
        self.circuit: Circuit = circuit #circuit
        self.gen_elms = circuit.generators # all generators
        self.load_elms = circuit.loads # all loads
        self.line_elms = circuit.transmission_lines # all lines
        self.trans_elms = circuit.transformers # all transformers
        self.bus_elms = circuit.buses # all buses
    #draws generators but not according to circuit
    def draw_gens(self):
        with sd.Drawing():
            for i, gen in enumerate(self.gen_elms.values()):
                label_real = str(gen.mw_setpoint) + " MW"
                elm.SourceV().up().label(label_real)

    #draws loads as two parallel boxes, one real, one imag
    def draw_loads(self):
        with sd.Drawing() as d:
            for i, load in enumerate(self.load_elms.values()):
                label_real = str(load.real_pwr) + " MW"
                label_imag = str(load.reactive_pwr) + " MVAR"
                real_load = elm.ResistorIEC().down().label(label_real)
                real_load.hold()
                elm.Line().right()
                imag_load = elm.ResistorVarIEC().down().label(label_imag)
                imag_load.hold()
                elm.Line().right()

    #not obsessed with where the line connects but oh well
    def draw_trans(self):
        with sd.Drawing() as d:
            for i, trans in enumerate(self.trans_elms.values()):
                label = trans.name
                xfmr = elm.Transformer().right().label(label)
                elm.Line().right().at(xfmr.s2).length(d.unit/4)

    def draw_lines(self):
        # start by defining the lines between the buses
        with sd.Drawing() as circ_draw: # main drawing
            for i, line in enumerate(self.line_elms.values()):
                in_bus = line.bus1.numBus-1 # index of bus where line originates
                out_bus = line.bus2.numBus-1 # index of bus where line inserts
                line_name = line.name # save line to bus_elms at location
                elm.Line().right().label(line_name)

    def draw_buses(self):
        with sd.Drawing() as d:
            for i, bus in enumerate(self.bus_elms.values()):
                elm.Dot().label(bus.name)
                d.move(dx = 2, dy = 0)



