import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPushButton, QMenu, QLabel, QVBoxLayout, QWidget
from GUI import GUI
from Circuit import Circuit

class MainWindow(QMainWindow):
    def __init__(self, circuit):
        super().__init__()
        title = QLabel("Circuit")
        font = title.font()
        font.setPointSize(30)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setCentralWidget(title)
        self.setWindowTitle("Circuit Simulator")
        bus_button = QPushButton("Add Bus")
        line_button =QPushButton("Add Line")
        trans_button = QPushButton("Add Transformer")
        gen_button = QPushButton("Add Generator")
        load_button = QPushButton("Load")

        layout = QVBoxLayout()
        layout.addWidget(bus_button)
        layout.addWidget(line_button)
        layout.addWidget(trans_button)
        layout.addWidget(gen_button)
        layout.addWidget(load_button)

        container = QWidget()
        container.setLayout(layout)

        bus_button.setCheckable(True)
        bus_button.clicked.connect(self.bus_button_e)

        line_button.setCheckable(True)
        line_button.clicked.connect(self.line_button_e)

        trans_button.setCheckable(True)
        trans_button.clicked.connect(self.trans_button_e)

        gen_button.setCheckable(True)
        gen_button.clicked.connect(self.gen_button_e)

        load_button.setCheckable(True)
        load_button.clicked.connect(self.load_button_e)

        self.setCentralWidget(container)
        self.circuit = circuit
        self.gui = GUI(circuit)

    def bus_button_e(self):
        print("Bus")
        self.gui.draw_buses()

    def line_button_e(self):
        print("Line")
        self.gui.draw_lines()

    def trans_button_e(self):
        print("Transformer")
        self.gui.draw_trans()

    def gen_button_e(self):
        print("Generator")
        self.gui.draw_gens()

    def load_button_e(self):
        print("Load")
        self.gui.draw_loads()


