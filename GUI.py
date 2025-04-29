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
        self.diagram = sd.Drawing()


    #draws generators but not according to circuit
    def draw_gens(self):
        with self.diagram: # main drawing
            for i, gen in enumerate(self.gen_elms.values()):
                label_real = str(gen.mw_setpoint) + " MW"
                elm.SourceV().up().label(label_real)

    #draws loads as two parallel boxes, one real, one imag
    def draw_loads(self):
        with self.diagram: # main drawing
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
        with self.diagram: # main drawing
            for i, trans in enumerate(self.trans_elms.values()):
                label = trans.name
                xfmr = elm.Transformer().right().label(label)
                elm.Line().right().at(xfmr.s2).length(self.diagram.unit/4)

    def draw_lines(self):
    # start by defining the lines between the buses
        with self.diagram: # main drawing
            for i, line in enumerate(self.line_elms.values()):
                in_bus = line.bus1.numBus-1 # index of bus where line originates
                out_bus = line.bus2.numBus-1 # index of bus where line inserts
                line_name = line.name # save line to bus_elms at location
                elm.Line().right().label(line_name)

    def draw_buses(self):
        with self.diagram:
            # for each bus junction, go through and see what is between
            stuff_attached_single = {}
            stuff_attached_double = {}

            for i, bus in enumerate(self.bus_elms.values()):
                stuff_attached_single[bus] = []
                stuff_attached_double[bus] = []

            # start with single terminal components
            for i, bus in enumerate(self.bus_elms.values()):
                for j, gen in enumerate(self.gen_elms.values()):
                    if gen.bus == bus:  # if generator is attached, append to matrix
                        stuff_attached_single[bus].extend([gen])
                for j, load in enumerate(self.load_elms.values()):  # if load is attached, append to matrix
                    if load.bus == bus: stuff_attached_single[bus].append(load)

                # now have to find the 2 terminal components
                for j, trans in enumerate(self.trans_elms.values()):  # if transformer is attached, append to matrix
                    if trans.bus1 == bus: stuff_attached_double[bus].append(trans)
                    if trans.bus2 == bus: stuff_attached_double[bus].append(trans)
                for j, line in enumerate(self.line_elms.values()):  # if line is attached, append to matrix
                    if line.bus1 == bus: stuff_attached_double[bus].append(line)
                    if line.bus2 == bus: stuff_attached_double[bus].append(line)


            #draw buses at evenly spaced intervals
            bus_dots = {} # to save buses

            for i, bus in enumerate(self.bus_elms.values()):
                bus_dots[bus] = {}

            for i, bus in enumerate(self.bus_elms.values()):
                position = (i*5, 0)
                dot = elm.Dot().at(position).label(bus.name)
                bus_dots[bus] = dot
                bus_dots[bus].location = position


            # Print the locations to verify
            for bus, dot in bus_dots.items():
                print(f"Bus: {bus.name}, Location: {dot.location}")

            # start at bus 1 and add single components
            for bus, stuff in stuff_attached_single.items(): # go through all buses
                #location of bus_dot
                loc = bus_dots[bus].location
                for component in stuff: #go through lists of components attached for single terminal
                        #Generators
                        if isinstance(component, Generator):
                            label_real = str(component.mw_setpoint) + " MW"
                            elm.SourceV().up().at(loc).label(label_real)

                        # #Loads
                        # if isinstance(component, Load):
                        #     label_real = str(component.real_pwr) + " MW"
                        #     label_imag = str(component.reactive_pwr) + " MVAR"
                        #     real_load = elm.ResistorIEC().down().at(loc).label(label_real)
                        #     real_load.hold()
                        #     elm.Line().right()
                        #     imag_load = elm.ResistorVarIEC().down().label(label_imag)
                        #     imag_load.hold()
                        #     elm.Line().right()


                # for bus, stuff in enumerate(stuff_attached_double.values()):
                #     for component in stuff:
                #         if isinstance(component, TransmissionLine):
                #             line_name = line.name  # save line to bus_elms at location
                #             elm.Line().right().label(line_name)
                #
                #         #Transformers
                #         if isinstance(component, Load):
                #             label_real = str(component.real_pwr) + " MW"
                #             label_imag = str(component.reactive_pwr) + " MVAR"
                #             real_load = elm.ResistorIEC().down().label(label_real)
                #             real_load.hold()
                #             elm.Line().right()
                #             imag_load = elm.ResistorVarIEC().down().label(label_imag)
                #             imag_load.hold()
                #             elm.Line().right()

