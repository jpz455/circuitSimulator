import sys
from webbrowser import Error

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QLabel, QVBoxLayout, QWidget, QTabWidget
from numpy.ma.core import power
import numpy as np

from GUI import GUI
from Bus import Bus
from Generator import Generator
from Geometry import Geometry
from Load import Load
from Solution import Solution
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Conductor import Conductor
from Bundle import Bundle
from Circuit import Circuit
from Settings import Settings, current_settings
from Fault import Fault


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Simulator")

        # initialize circuit
        self.circuit = Circuit("circuit", current_settings)
        self.conductor: Conductor
        self.bundle: Bundle
        self.geometry: Geometry
        self.line_setup_done: bool = False  # tracks if line setup is initialized

        #create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.create_add_components_tab()
        self.create_solve_circuit_tab()
        self.create_solve_faults_tab()
        self.create_test_tab()

        self.errorLabel = QLabel()

    def bus_button_e(self):

        #uncheck all other buttons, check this one
        self.set_checked_component_button(self.bus_button)
        # get user inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter bus name: ')
        base = QtWidgets.QInputDialog.getInt(self, 'Base Voltage', 'Enter bus voltage base (kV): ')
        type = QtWidgets.QInputDialog.getText(self, 'Type', 'Enter bus type: ')
        v = QtWidgets.QInputDialog.getDouble(self, 'Voltage', 'Enter bus voltage (pu): ', decimals = 5)
        delta = QtWidgets.QInputDialog.getDouble(self, 'Delta', 'Enter bus delta (deg): ', decimals = 5)
        bus = Bus(name[0], base[0], type[0], v[0], delta[0])

        # add bus to circuit
        self.circuit.add_bus(bus)

        #uncheck button
        self.uncheck_button(self.bus_button)

        #update output
        self.update_circuit_elements("bus")

    def line_button_e(self):

        # uncheck all other buttons, check this one
        self.set_checked_component_button(self.line_button)

        # get user inputs

        #get set up if not already given
        if not self.line_setup_done:
            self.bundle, self.geometry = self.setup_lines()

        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter transmission line name: ')
        bus1_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus 1 name: ')
        bus2_name = QtWidgets.QInputDialog.getText(self, 'Bus 2', 'Enter bus 2 name: ')
        length = QtWidgets.QInputDialog.getDouble(self, 'Length', 'Enter transmission line length (mi): ', decimals = 5)

        # get bus from circuit
        bus1 = self.circuit.buses[bus1_name[0]]
        bus2 = self.circuit.buses[bus2_name[0]]

        # add line
        line = TransmissionLine(name[0], bus1, bus2, self.bundle, self.geometry, length[0])

        # uncheck button
        self.uncheck_button(self.line_button)

        # add to circuit
        self.circuit.add_transmission_line(line)
        self.update_circuit_elements("line")

    def trans_button_e(self):

        # uncheck all other buttons, check this one
        self.set_checked_component_button(self.trans_button)

        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter transformer name: ')
        bus1_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus 1 name: ')
        bus2_name = QtWidgets.QInputDialog.getText(self, 'Bus 2', 'Enter bus 2 name: ')
        power_rating = QtWidgets.QInputDialog.getDouble(self, 'Length', 'Enter power rating (MW): ', decimals = 5)
        z_per = QtWidgets.QInputDialog.getDouble(self, 'Impedance Percent', 'Enter impedance percentage: ', decimals = 5)
        x_over_r = QtWidgets.QInputDialog.getDouble(self, 'X over R Ratio', 'Enter x over r ratio: ', decimals = 5)
        connection = QtWidgets.QInputDialog.getText(self, 'Connection', 'Enter connection type: ')
        ground = QtWidgets.QInputDialog.getDouble(self, 'Grounding Reactance', 'Enter grounding reactance: ', decimals = 5)

        # get bus from circuit
        bus1 = self.circuit.buses[bus1_name[0]]
        bus2 = self.circuit.buses[bus2_name[0]]

        #add transformer
        transformer = Transformer(name[0], bus1, bus2, power_rating[0], z_per[0], x_over_r[0], connection[0], ground[0])
        self.circuit.add_transformer(transformer)
        self.update_circuit_elements("trans")

        # uncheck button
        self.uncheck_button(self.trans_button)

    def gen_button_e(self):

        # uncheck all other buttons, check this one
        self.set_checked_component_button(self.gen_button)

        # get inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter generator name: ')
        bus_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus name: ')
        v_set = QtWidgets.QInputDialog.getDouble(self, 'Voltage Set Point', 'Enter voltage set point (kV): ', decimals = 5)
        mw_set = QtWidgets.QInputDialog.getDouble(self, 'Power Set Point', 'Enter power set point (MW): ', decimals = 5)
        x1 = QtWidgets.QInputDialog.getDouble(self, 'X1', 'Enter X1: ', decimals = 5)
        x2 = QtWidgets.QInputDialog.getDouble(self, 'X2', 'Enter X2: ', decimals = 5)
        x3 = QtWidgets.QInputDialog.getDouble(self, 'X3', 'Enter X3: ', decimals = 5)
        ground_x = QtWidgets.QInputDialog.getDouble(self, 'Grounding X', 'Enter grounding reactance: ', decimals = 5)
        ground_bool = QtWidgets.QInputDialog.getText(self, 'Grounded', 'Enter t if grounded, f if false : ')

        #set grounded or not
        if ground_bool[0] == 't':
            set_ground = True
        elif ground_bool[0] == 'f':
            set_ground = False
        else:
            set_ground = False
            print("Defaulting to ungrounded")

        #get bus
        bus = self.circuit.buses[bus_name[0]]

        #make generator
        generator = Generator(name[0], bus, v_set[0], mw_set[0], x1[0], x2[0], x3[0], ground_x[0], set_ground, current_settings)


        #add generator
        self.circuit.add_generator(generator)
        self.update_circuit_elements("gen")

        # uncheck button
        self.uncheck_button(self.gen_button)

    def load_button_e(self):
        # uncheck all other buttons, check this one
        self.set_checked_component_button(self.load_button)

        # get inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter load name: ')
        bus_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus name: ')
        q = QtWidgets.QInputDialog.getDouble(self, 'Reactive Power', 'Enter reactive power (MVAR): ', decimals = 5)
        p = QtWidgets.QInputDialog.getDouble(self, 'Real Power', 'Enter real power (MW): ', decimals = 5)

        # get bus
        bus = self.circuit.buses[bus_name[0]]

        # make load
        load = Load(name[0], bus, p[0], q[0], current_settings)

        # add load
        self.circuit.add_load(load)
        self.update_circuit_elements("load")

        # uncheck button
        self.uncheck_button(self.load_button)

    def setup_lines(self):
        # get basic inputs for lines
        #conductor
        d = QtWidgets.QInputDialog.getDouble(self, 'Diameter', 'Enter conductor diameter: ', decimals = 5)
        GMR = QtWidgets.QInputDialog.getDouble(self, 'GMR', 'Enter conductor GMR: ', decimals = 5)
        r = QtWidgets.QInputDialog.getDouble(self, 'Resistance', 'Enter conductor resistance: ', decimals = 5)
        amp = QtWidgets.QInputDialog.getDouble(self, 'Amperage', 'Enter conductor amperage: ', decimals = 5)
        self.conductor = Conductor('conductor', d[0], GMR[0], r[0], amp[0])
        self.circuit.add_conductor(self.conductor)

        # get bundle
        num = QtWidgets.QInputDialog.getInt(self, 'Number', 'Enter number of conductors : ')
        spacing = QtWidgets.QInputDialog.getDouble(self, 'Spacing', 'Enter conductor spacing : ')
        self.bundle = Bundle('bundle', num[0], spacing[0], self.conductor)

        # get geometry
        xa = QtWidgets.QInputDialog.getDouble(self, 'XA', 'Enter phase A x position: ', decimals = 5)
        xb = QtWidgets.QInputDialog.getDouble(self, 'XB', 'Enter phase B x position: ', decimals = 5)
        xc = QtWidgets.QInputDialog.getDouble(self, 'XC', 'Enter phase C x position: ', decimals = 5)
        ya = QtWidgets.QInputDialog.getDouble(self, 'YA', 'Enter phase A y position: ', decimals = 5)
        yb = QtWidgets.QInputDialog.getDouble(self, 'YB', 'Enter phase B y position: ', decimals = 5)
        yc = QtWidgets.QInputDialog.getDouble(self, 'YC', 'Enter phase C y position: ', decimals = 5)

        #set setup bool as true
        self.line_setup_done = True

        # create geometry
        self.geometry = Geometry("geometry", xa[0], ya[0], xb[0], yb[0], xc[0], yc[0])
        self.circuit.add_geometry(self.geometry)

        return self.bundle, self.geometry

    def set_checked_component_button(self, button):
        # ensures that only the clicked button is active
        button.setChecked(True)
        button.setEnabled(False)
        for b in self.component_buttons:
            if b != button:
                b.setChecked(False)
                b.setEnabled(True)

    def uncheck_button(self, button):
        # uncheck button
        button.setChecked(False)
        button.setCheckable(True)
        button.setEnabled(True)

    def update_circuit_elements(self, component_type):
        #get the updated buses

        if component_type == "bus":
            bus_details = ["Buses:"]
            for bus in self.circuit.buses.values():
                details = f"Name: {bus.name}, Base: {bus.base_kv}, Type: {bus.bus_type}, V_pu: {bus.v_pu}, Delta: {bus.delta}"
                bus_details.append(details)
            bus_label = "\n".join(bus_details)
            self.bus_label.setText(bus_label)

        elif component_type == "line":
            #get updated lines
            line_details = ["Lines:"]
            for line in self.circuit.transmission_lines.values():
                details = f"Name: {line.name}, Bus 1: {line.bus1.name}, Bus 2: {line.bus2.name}, Length: {line.length}"
                line_details.append(details)
            line_label = "\n".join(line_details)
            self.line_label.setText(line_label)

        elif component_type == "trans":
            #get updated transformers
            trans_details = ["Transformers:"]
            for trans in self.circuit.transformers.values():
                details = f"Name: {trans.name}, Bus 1: {trans.bus1.name}, Bus 2: {trans.bus2.name}, Power Rating: {trans.power_rating}"
                trans_details.append(details)
            trans_label = "\n".join(trans_details)
            self.trans_label.setText(trans_label)

        elif component_type == "gen":
            #get updated gens
            gen_details = ["Generators:"]
            for gen in self.circuit.generators.values():
                details = f"Name: {gen.name}, Voltage Setpoint: {gen.voltage_setpoint}, Power Setpoint: {gen.mw_setpoint}"
                gen_details.append(details)
            gen_label = "\n".join(gen_details)
            self.gen_label.setText(gen_label)

        elif component_type == "load":
            #get updated loads
            load_details = ["Loads:"]
            for load in self.circuit.loads.values():
                details = f"Name: {load.name}, Real Power: {load.real_pwr}, Reactive Power: {load.reactive_pwr}"
                load_details.append(details)
            load_label = "\n".join(load_details)
            self.load_label.setText(load_label)

    def create_add_components_tab(self):
        # create tab and layout
        add_components_tab = QWidget()
        layout = QVBoxLayout()

        # buttons
        self.bus_button = QPushButton("Add Bus")
        self.line_button = QPushButton("Add Line")
        self.trans_button = QPushButton("Add Transformer")
        self.gen_button = QPushButton("Add Generator")
        self.load_button = QPushButton("Add Load")

        # labels
        self.bus_label = QLabel("Buses:")
        self.line_label = QLabel("Transmission Lines:")
        self.trans_label = QLabel("Transformers:")
        self.gen_label = QLabel("Generators:")
        self.load_label = QLabel("Loads:")

        # list of buttons
        self.component_buttons = [self.bus_button, self.line_button, self.trans_button, self.gen_button, self.load_button]

        # add to layout
        layout.addWidget(self.bus_button)
        layout.addWidget(self.line_button)
        layout.addWidget(self.trans_button)
        layout.addWidget(self.gen_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.bus_label)
        layout.addWidget(self.line_label)
        layout.addWidget(self.trans_label)
        layout.addWidget(self.gen_label)
        layout.addWidget(self.load_label)

        # set up buttons
        # set checkable
        for button in self.component_buttons:
            button.setCheckable(True)

        # connect signals
        self.bus_button.clicked.connect(self.bus_button_e)
        self.line_button.clicked.connect(self.line_button_e)
        self.trans_button.clicked.connect(self.trans_button_e)
        self.gen_button.clicked.connect(self.gen_button_e)
        self.load_button.clicked.connect(self.load_button_e)

        # add layout to tab
        add_components_tab.setLayout(layout)

        # add tab to main window
        self.tabs.addTab(add_components_tab, "Add Components")

    def create_solve_circuit_tab(self):
        # create tab and layout
        self.solve_circuit_tab = QWidget()
        layout = QVBoxLayout()

        # button
        self.solve_button = QPushButton("Solve Power Flow")

        # labels
        self.solution_current_label = QLabel("Solution Current")
        self.solution_voltage_label = QLabel("Solution Voltage")


        # set up button
        self.solve_button.setCheckable(True)
        self.solve_button.clicked.connect(self.solve_button_e)

        # add to layout
        layout.addWidget(self.solve_button)
        layout.addWidget(self.solution_current_label)
        layout.addWidget(self.solution_voltage_label)

        # add layout to tab
        self.solve_circuit_tab.setLayout(layout)

        # add tab to main window
        self.tabs.addTab(self.solve_circuit_tab, "Solve Power Flow")

    def create_solve_faults_tab(self):
        # create tab and layout
        self.fault_study_tab = QWidget()
        layout = QVBoxLayout()

        # buttons
        self.fault_bus_button = QPushButton("Fault Bus")
        self.balanced_fault_button = QPushButton("3 Phase Balanced Fault")
        self.line_to_line_fault_button = QPushButton("Line Fault")
        self.single_line_fault_button = QPushButton("Single Line to Ground Fault")
        self.double_line_fault_button = QPushButton("Double Line to Ground Fault")

        # labels
        self.fault_current_label = QLabel("Fault Current")
        self.fault_voltage_label = QLabel("Fault Voltage")

        # lists
        self.fault_buttons = [self.fault_bus_button, self.line_to_line_fault_button, self.single_line_fault_button, self.double_line_fault_button]

        # connect signals
        self.fault_bus_button.clicked.connect(self.fault_bus_button_e)
        self.balanced_fault_button.clicked.connect(self.balanced_fault_button_e)
        self.line_to_line_fault_button.clicked.connect(self.line_to_line_fault_button_e)
        self.single_line_fault_button.clicked.connect(self.single_line_fault_button_e)
        self.double_line_fault_button.clicked.connect(self.double_line_fault_button_e)


        # add to layout
        layout.addWidget(self.fault_bus_button)
        layout.addWidget(self.balanced_fault_button)
        layout.addWidget(self.line_to_line_fault_button)
        layout.addWidget(self.single_line_fault_button)
        layout.addWidget(self.double_line_fault_button)
        layout.addWidget(self.fault_current_label)
        layout.addWidget(self.fault_voltage_label)

        # add layout to tab
        self.fault_study_tab.setLayout(layout)

        # add tab to main window
        self.tabs.addTab(self.fault_study_tab, "Fault Study")

    def solve_button_e(self):
        # check button
        self.solve_button.setChecked(True)
        print(self.circuit.buses.keys())
        print(self.circuit.transformers.keys())
        print(self.circuit.generators.keys())
        print(self.circuit.loads.keys())
        print(self.circuit.transmission_lines.keys())


        # solve circuit
        # set up solution
        self.solution = Solution(self.circuit)
        self.solution.calc_known_power()
        self.solution.calc_mismatch()
        jacob = self.solution.calc_jacobian()

        # solve and save voltages
        # try:
        #     voltage_matrix = self.solution.calc_solution()
        # except Exception as e:
        #     self.errorLabel.setText(e)
        #     voltage_matrix = None

        #print voltages to label
        v_label = ("Solution found\nVpu        Angle(degrees)\n", jacob)
        self.solution_voltage_label.setText(v_label)

        # uncheck button
        self.solve_button.setChecked(False)
        self.solve_button.setCheckable(True)
        self.solve_button.setEnabled(True)

    def fault_bus_button_e(self):
        # set checked button, uncheck all others
        self.set_checked_fault_button(self.fault_bus_button)

        # prompt user to provide fault bus & fault voltage
        self.fault_bus_name, ok = QtWidgets.QInputDialog.getText(self, 'Fault Bus', 'Enter name of fault bus: ')
        self.fault_v, ok2 = QtWidgets.QInputDialog.getDouble(self, 'Fault Voltage', 'Enter fault voltage: ', decimals=5)

        # uncheck button
        self.uncheck_button(self.fault_bus_button)

    def balanced_fault_button_e(self):
        # check button, uncheck others
        self.set_checked_fault_button(self.balanced_fault_button)

        # initialize fault study
        self.fault = Fault(self.circuit)

        # call fault method to solve balanced fault
        V, I = self.fault.calc_3_phase_bal(self.fault_bus_name, self.fault_v)

        # populate labels
        fault_i_out = "Fault Current Magnitude: ", round(np.real(I), 5)
        fault_v_out = ""

        for i, v in enumerate(V):
            fault_v_out += f"Bus {i + 1} voltage magnitude: {v}\n"

        self.fault_voltage_label.setText(str)

        # uncheck
        self.uncheck_button(self.balanced_fault_button)

    def line_to_line_fault_button_e(self):
        # check button, uncheck others
        self.set_checked_fault_button(self.line_to_line_fault_button)

        # initialize fault study
        self.fault = Fault(self.circuit)

        # call fault method to solve balanced fault
        V, I = self.fault.calc_line_to_line(self.fault_bus_name, self.fault_v)

        for bus in self.circuit.buses:
            for v, phase in enumerate(['A', 'B', 'C']):
                str = (f"{bus} Phase {phase}: |V| = {np.abs(V[v]):.4f} p.u., ∠ = {np.angle(V[v], deg=True):.2f}°")

        self.fault_voltage_label.setText(str)

        # uncheck
        self.uncheck_button(self.balanced_fault_button)
    def single_line_fault_button_e(self):
        pass
    def double_line_fault_button_e(self):
        pass
    def set_checked_fault_button(self, button):
        # ensures that only the clicked button is active
        button.setChecked(True)
        button.setEnabled(False)
        for b in self.fault_buttons:
            if b != button:
                b.setChecked(False)
                b.setEnabled(True)

    def create_test_tab(self):
        # create tab and layout
        self.test_tab = QWidget()
        layout = QVBoxLayout()

        # button
        self.test_circuit_button = QPushButton("Load Test Circuit")

        # labels
        self.test_circuit_label = QLabel("Test Circuit Values:")
        self.test_buses_label = QLabel("Test Circuit Buses:")
        self.test_trans_label = QLabel("Test Circuit Transformers:")
        self.test_lines_label = QLabel("Test Circuit Lines:")
        self.test_gens_label = QLabel("Test Circuit Generators:")
        self.test_loads_label = QLabel("Test Circuit Loads:")

        # set up button
        self.test_circuit_button.setCheckable(True)
        self.test_circuit_button.clicked.connect(self.test_circuit_button_e)

        # add to layout
        layout.addWidget(self.test_circuit_button)
        layout.addWidget(self.test_buses_label)
        layout.addWidget(self.test_trans_label)
        layout.addWidget(self.test_lines_label)
        layout.addWidget(self.test_gens_label)
        layout.addWidget(self.test_loads_label)

        # add layout to tab
        self.test_tab.setLayout(layout)

        # add tab to main window
        self.tabs.addTab(self.test_tab, "Load Test Circuit")

    def test_circuit_button_e(self):
        # loads in 7 bus circuit to avoid having to retype everytime
        # set checked
        self.test_circuit_button.setChecked(True)

        # load all the buses
        bus1 = Bus("bus1", 20, "slack")
        bus2 = Bus("bus2", 230, "pq", )
        bus3 = Bus("bus3", 230, "pq")
        bus4 = Bus("bus4", 230, "pq")
        bus5 = Bus("bus5", 230, "pq")
        bus6 = Bus("bus6", 230, "pq")
        bus7 = Bus("bus7", 18, "pv")

        self.circuit.add_bus(bus1)
        self.circuit.add_bus(bus2)
        self.circuit.add_bus(bus3)
        self.circuit.add_bus(bus4)
        self.circuit.add_bus(bus5)
        self.circuit.add_bus(bus6)
        self.circuit.add_bus(bus7)

        # load all the transformers
        T1 = Transformer("T1", bus1, bus2, 125, 8.5, 10, 'delta-y', 1)
        T2 = Transformer("T2", bus6, bus7, 200, 10.5, 12, 'delta-y', 0)

        self.circuit.add_transformer(T1)
        self.circuit.add_transformer(T2)

        # load all the lines
        conductor1 = Conductor("Partridge", .642, .0217, .385, 460)
        self.circuit.add_conductor(conductor1)

        geometry1 = Geometry("G1", 0, 0, 19.5, 0, 39, 0)
        self.circuit.add_geometry(geometry1)
        bundle1 = Bundle('B1', 2, 1.5, conductor1)

        tLine1 = TransmissionLine("tline1", bus2, bus4, bundle1, geometry1, 10)
        tLine2 = TransmissionLine("tline2", bus2, bus3, bundle1, geometry1, 25)
        tLine3 = TransmissionLine("tline3", bus3, bus5, bundle1, geometry1, 20)
        tLine4 = TransmissionLine("tline4", bus4, bus6, bundle1, geometry1, 20)
        tLine5 = TransmissionLine("tline5", bus5, bus6, bundle1, geometry1, 10)
        tLine6 = TransmissionLine("tline6", bus4, bus5, bundle1, geometry1, 35)

        self.circuit.add_transmission_line(tLine1)
        self.circuit.add_transmission_line(tLine2)
        self.circuit.add_transmission_line(tLine3)
        self.circuit.add_transmission_line(tLine4)
        self.circuit.add_transmission_line(tLine5)
        self.circuit.add_transmission_line(tLine6)

        # load the generators
        gen1 = Generator("Gen 1", bus1, 0, 100, .12, .14, .05, 0, True, current_settings)
        self.circuit.add_generator(gen1)
        gen2 = Generator("Gen 2", bus7, 0, 200, .12, .14, .05, .01, True, current_settings)
        self.circuit.add_generator(gen2)

        # load the loads
        load1 = Load("load1", bus3, -110, -50, current_settings)
        self.circuit.add_load(load1)
        load2 = Load("load2", bus4, -100, -70, current_settings)
        self.circuit.add_load(load2)
        load3 = Load("load3", bus5, -100, -65, current_settings)
        self.circuit.add_load(load3)

        # update all the things
        bus_details = ["Buses:"]
        for bus in self.circuit.buses.values():
            details = f"Name: {bus.name}, Base: {bus.base_kv}, Type: {bus.bus_type}, V_pu: {bus.v_pu}, Delta: {bus.delta}"
            bus_details.append(details)
        bus_label = "\n".join(bus_details)
        self.test_buses_label.setText(bus_label)

        line_details = ["Lines:"]
        for line in self.circuit.transmission_lines.values():
            details = f"Name: {line.name}, Bus 1: {line.bus1.name}, Bus 2: {line.bus2.name}, Length: {line.length}"
            line_details.append(details)
        line_label = "\n".join(line_details)
        self.test_lines_label.setText(line_label)

        trans_details = ["Transformers:"]
        for trans in self.circuit.transformers.values():
            details = f"Name: {trans.name}, Bus 1: {trans.bus1.name}, Bus 2: {trans.bus2.name}, Power Rating: {trans.power_rating}"
            trans_details.append(details)
        trans_label = "\n".join(trans_details)
        self.test_trans_label.setText(trans_label)

        gen_details = ["Generators:"]
        for gen in self.circuit.generators.values():
            details = f"Name: {gen.name}, Voltage Setpoint: {gen.voltage_setpoint}, Power Setpoint: {gen.mw_setpoint}"
            gen_details.append(details)
        gen_label = "\n".join(gen_details)
        self.test_gens_label.setText(gen_label)

        load_details = ["Loads:"]
        for load in self.circuit.loads.values():
            details = f"Name: {load.name}, Real Power: {load.real_pwr}, Reactive Power: {load.reactive_pwr}"
            load_details.append(details)
        load_label = "\n".join(load_details)
        self.test_loads_label.setText(load_label)


