import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPushButton, QMenu, QLabel


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

    def add_menu(self, e):
        context = QMenu(self)
        context.addAction(QAction('Add Bus', self))
        context.addAction(QAction('Add Line', self))
        context.addAction(QAction('Add Transformer', self))
        context.addAction(QAction('Add Generator', self))
        context.addAction(QAction('Add Load', self))
        context.exec(e.globalPos())

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()