# Built-in module
import sys
import os
from vision import camera1
from vision import camera2

# PyQt5 Module
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Other Module

path = os.path.dirname(os.path.abspath('robot-camera'))
print(path)


class CalibrationGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.path_ui = path + "/views/calibration-gui.ui"

        loadUi(self.path_ui, self)

        self.time = QTimer(self)

        self.cameraCBox.addItem(camera1.name)
        self.cameraCBox.addItem(camera2.name)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_window = CalibrationGUI()
    main_window.setWindowTitle('Color Calibration App')

    main_window.show()
    sys.exit(app.exec())
# lower = [110, 150, 20]
# upper = [120, 255, 255]

# camera2.set_lower(lower)
# camera2.set_upper(upper)
# camera2.open_camera_stream()
