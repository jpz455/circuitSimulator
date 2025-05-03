import sys

from PyQt5.QtWidgets import QApplication
from Window import MainWindow

# Main function: opens GUI window
app = QApplication(sys.argv)
window = MainWindow()
window.show()
try:
    sys.exit(app.exec_())
except Exception as e:
    print("Error", e)


