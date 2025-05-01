import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPushButton, QMenu, QLabel, QVBoxLayout, QWidget
from numpy.ma.core import power

from GUI import GUI
from Bus import Bus
from Generator import Generator
from Geometry import Geometry
from Load import Load
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Conductor import Conductor
from Bundle import Bundle
from Circuit import Circuit
from Settings import Settings, current_settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        title = QLabel("Circuit")
        font = title.font()
        font.setPointSize(30)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setCentralWidget(title)
        self.setWindowTitle("Circuit Simulator")
        self.bus_button = QPushButton("Add Bus")
        self.line_button =QPushButton("Add Line")
        self.trans_button = QPushButton("Add Transformer")
        self.gen_button = QPushButton("Add Generator")
        self.load_button = QPushButton("Load")

        layout = QVBoxLayout()
        layout.addWidget(self.bus_button)
        layout.addWidget(self.line_button)
        layout.addWidget(self.trans_button)
        layout.addWidget(self.gen_button)
        layout.addWidget(self.load_button)

        container = QWidget()
        container.setLayout(layout)

        self.bus_button.setCheckable(True)
        self.bus_button.clicked.connect(self.bus_button_e)

        self.line_button.setCheckable(True)
        self.line_button.clicked.connect(self.line_button_e)

        self.trans_button.setCheckable(True)
        self.trans_button.clicked.connect(self.trans_button_e)

        self.gen_button.setCheckable(True)
        self.gen_button.clicked.connect(self.gen_button_e)

        self.load_button.setCheckable(True)
        self.load_button.clicked.connect(self.load_button_e)

        self.setCentralWidget(container)
        self.circuit = Circuit("circuit", Settings)

    def bus_button_e(self):
        # get user inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter bus name: ')
        base = QtWidgets.QInputDialog.getInt(self, 'Base', 'Enter bus base: ')
        type = QtWidgets.QInputDialog.getText(self, 'Type', 'Enter bus type: ')
        v = QtWidgets.QInputDialog.getDouble(self, 'Voltage', 'Enter bus voltage: ')
        delta = QtWidgets.QInputDialog.getDouble(self, 'Delta', 'Enter bus delta: ')
        bus = Bus(name[0], base[0], type[0], v[0], delta[0])
        # add bus to circuit
        self.circuit.add_bus(bus)
        print("Bus added")

    def line_button_e(self):
        # get user inputs
        bundle, geometry = self.set_up()

        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter transmission line name: ')
        bus1_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus 1 name: ')
        bus2_name = QtWidgets.QInputDialog.getText(self, 'Bus 2', 'Enter bus 2 name: ')
        length = QtWidgets.QInputDialog.getDouble(self, 'Length', 'Enter transmission line length: ')

        # get bus from circuit
        bus1 = self.circuit.buses[bus1_name[0]]
        bus2 = self.circuit.buses[bus2_name[0]]

        # add line
        line = TransmissionLine(name[0], bus1, bus2, bundle, geometry, length[0])

        # add to circuit
        self.circuit.add_transmission_line(line)
        print("Transmission line added")

    def trans_button_e(self):

        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter transformer name: ')
        bus1_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus 1 name: ')
        bus2_name = QtWidgets.QInputDialog.getText(self, 'Bus 2', 'Enter bus 2 name: ')
        power_rating = QtWidgets.QInputDialog.getDouble(self, 'Length', 'Enter power rating (MW): ')
        z_per = QtWidgets.QInputDialog.getDouble(self, 'Impedance Percent', 'Enter impedance percentage: ')
        x_over_r = QtWidgets.QInputDialog.getDouble(self, 'X over R Ratio', 'Enter x over r ratio: ')
        connection = QtWidgets.QInputDialog.getText(self, 'Connection', 'Enter connection type: ')
        ground = QtWidgets.QInputDialog.getText(self, 'Grounding Reactance', 'Enter grounding reactance: ')

        # get bus from circuit
        bus1 = self.circuit.buses[bus1_name[0]]
        bus2 = self.circuit.buses[bus2_name[0]]

        #add transformer
        transformer = Transformer(name[0], bus1, bus2, power_rating[0], z_per[0], x_over_r[0], connection[0], ground[0])
        self.circuit.add_transformer(transformer)

        #print
        print("Transformer added")

    def gen_button_e(self):
        #get inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter generator name: ')
        bus_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus name: ')
        v_set = QtWidgets.QInputDialog.getDouble(self, 'Voltage Set Point', 'Enter voltage set point (kV): ')
        mw_set = QtWidgets.QInputDialog.getDouble(self, 'Power Set Point', 'Enter power set point (MW): ')
        x1 = QtWidgets.QInputDialog.getDouble(self, 'X1', 'Enter X1: ')
        x2 = QtWidgets.QInputDialog.getDouble(self, 'X2', 'Enter X2: ')
        x3 = QtWidgets.QInputDialog.getDouble(self, 'X3', 'Enter X3: ')
        ground_x = QtWidgets.QInputDialog.getDouble(self, 'Grounding X', 'Enter grounding reactance: ')
        ground_bool = QtWidgets.QInputDialog.getText(self, 'Grounded', 'Enter t if grounded, f if false : ')

        #set grounded or not
        if ground_bool == 't':
            ground_bool = True
        else:
            ground_bool = False

        #get bus
        bus = self.circuit.buses[bus_name[0]]

        #make generator
        generator = Generator(name, bus, v_set, mw_set, x1, x2, x3, ground_x, ground_bool)

        #add generator
        self.circuit.add_generator(generator)
        print("Generator Added")

    def load_button_e(self):
        # get inputs
        name = QtWidgets.QInputDialog.getText(self, 'Name', 'Enter generator name: ')
        bus_name = QtWidgets.QInputDialog.getText(self, 'Bus 1', 'Enter bus name: ')
        q = QtWidgets.QInputDialog.getDouble(self, 'Reactive Power', 'Enter reactive power (MVAR): ')
        p = QtWidgets.QInputDialog.getDouble(self, 'Real Power', 'Enter real power (MW): ')

        # get bus
        bus = self.circuit.buses[bus_name[0]]

        # make load
        load = Load(name[0], bus, p[0], q[0], current_settings)

        # add load
        self.circuit.add_generator(load)
        print("Load Added")


    def set_up(self):
        # get basic inputs for lines
        d = QtWidgets.QInputDialog.getDouble(self, 'Diameter', 'Enter conductor diameter: ')
        GMR = QtWidgets.QInputDialog.getDouble(self, 'GMR', 'Enter conductor GMR: ')
        r = QtWidgets.QInputDialog.getDouble(self, 'Resistance', 'Enter conductor resistance: ')
        amp = QtWidgets.QInputDialog.getDouble(self, 'Amperage', 'Enter conductor amperage: ')
        conductor = Conductor('conductor', d[0], GMR[0], r[0], amp[0])

        # get bundle
        num = QtWidgets.QInputDialog.getInt(self, 'Number', 'Enter number of conductors : ')
        spacing = QtWidgets.QInputDialog.getDouble(self, 'Spacing', 'Enter conductor spacing : ')
        bundle = Bundle('bundle', num[0], spacing[0], conductor)

        # get geometry
        xa = QtWidgets.QInputDialog.getDouble(self, 'XA', 'Enter phase A x position: ')
        xb = QtWidgets.QInputDialog.getDouble(self, 'XB', 'Enter phase B x position: ')
        xc = QtWidgets.QInputDialog.getDouble(self, 'XC', 'Enter phase C x position: ')
        ya = QtWidgets.QInputDialog.getDouble(self, 'YA', 'Enter phase A y position: ')
        yb = QtWidgets.QInputDialog.getDouble(self, 'YB', 'Enter phase B y position: ')
        yc = QtWidgets.QInputDialog.getDouble(self, 'YC', 'Enter phase C y position: ')

        # create geometry
        geometry = Geometry("geometry", xa[0], ya[0], xb[0], yb[0], xc[0], yc[0])

        return bundle, geometry


