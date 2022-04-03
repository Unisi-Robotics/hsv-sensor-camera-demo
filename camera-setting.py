# Built-in module
from vision import camera1
from vision import camera2

# PyQt5 Module
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage

# Other Module
import sys
import os
import imutils

path = os.path.dirname(os.path.abspath('robot-camera'))
print(path)


class CalibrationGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.path_ui = path + "/views/calibration-gui.ui"

        loadUi(self.path_ui, self)

        self.timer = QTimer(self)
        self.pixmap = None
        self.frame = []
        self.camera = camera2

        self.cameraCBox.addItem(camera1.name)
        self.cameraCBox.addItem(camera2.name)

        self.timer.start(1)

        self.play_button_clicked()

    def display_frame(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        out_image = QImage(img, img.shape[1],
                           img.shape[0], img.strides[0], qformat)
        #BGR >> RGB
        out_image = out_image.rgbSwapped()

        self.pixmap = QPixmap.fromImage(out_image)
        self.videoFrame.setPixmap(self.pixmap)
        self.videoFrame.setScaledContents(True)

    def play_button_clicked(self):
        text = self.playButton.text()
        if text == "Play":
            self.start_timer(self.update_frame)
            self.playButton.setText('Stop')
        elif text == 'Stop':
            self.stop_timer(self.update_frame)
            self.playButton.setText('Play')

    def update_frame(self):
        if self.camera is not None:
            self.frame = self.camera.get_frame()
            self.frame = imutils.resize(self.frame, height=480)
            self.display_frame(self.frame)

    def start_timer(self, callback):
        try:
            self.timer.timeout.disconnect(callback)
        except:
            pass
        self.timer.timeout.connect(callback)

    def stop_time(self, callback=None):
        if callback is None:
            self.timer.stop(())
        else:
            try:
                self.timer.timeout.disconnect(callback)
            except:
                pass


if __name__ == "__main__":

    try:
        app = QApplication(sys.argv)
        main_window = CalibrationGUI()
        main_window.setWindowTitle('Color Calibration App')

        main_window.show()
        sys.exit(app.exec())

    except Exception as e:
        print('Exiting Application')
