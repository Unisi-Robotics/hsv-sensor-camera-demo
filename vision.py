import cv2 as cv
import numpy as np
import v4l2
import fcntl


class Camera:

    def __init__(self, devices, name, onFrame=True, lower_val=None, upper_val=None):

        if lower_val is None or upper_val is None:
            self.lower_val = [0, 0, 0]
            self.upper_val = [1, 1, 1]

        else:
            self.lower_val = lower_val
            self.upper_val = upper_val

        self.devices = devices
        self.cam = f'/dev/video{str(self.devices)}'
        self.cam_file = open(f'/dev/video{str(self.devices)}', 'r')
        self.name = name

        if onFrame:
            self.cap = cv.VideoCapture(self.cam)

    def set_lowerHSV(self, lower):
        self.lower_val[0] = lower[0]
        self.lower_val[1] = lower[1]
        self.lower_val[2] = lower[2]

    def set_upperHSV(self, upper):
        self.upper_val[0] = upper[0]
        self.upper_val[1] = upper[1]
        self.upper_val[2] = upper[2]

    def get_frame(self):

        frame = []

        try:
            _, frame = self.cap.read()

            self.upper_val = np.asarray(self.upper_val)
            self.lower_val = np.asarray(self.lower_val)

            frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(frame, self.lower_val, self.upper_val)

        except Exception as e:
            print('get frame', e)

        return frame

    def set_control(self, arg):
        control = v4l2.v4l2_control()
        qcontrol = v4l2.v4l2_queryctrl()

        try:
            qcontrol.id = getattr(v4l2, arg)
            fcntl.ioctl(self.cam, v4l2.VIDIOC_QUERYCTRL, qcontrol)
            control.id = getattr(self.cam, v4l2.VIDIOC_G_CTRL, control)
            return {'min': qcontrol.minimum, 'max': qcontrol.maximum, 'default': qcontrol.default, 'value': control.value}

        except Exception as e:
            print(f'{arg} is not supported')

        return None


try:
    camera1 = Camera(0, 'Camera:0')
except Exception as e:
    print('Camera:0', e)

try:
    camera2 = Camera(2, 'Camera:1')
except Exception as e:
    print('Camera:1', e)

if __name__ == "__main__":

    """
        NOTE:
        Yellow: lower: [15, 150, 20], upper: [35, 255, 255]
        Dark Blue: lower: [15, 150, 20], upper: [35, 255, 255]

    """

    pass

    while True:
        frame = camera2.get_frame()

        cv.imshow('Test Camera', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # lower = [110, 150, 20]
    # upper = [120, 255, 255]

    # camera1 = Camera(0, lower, upper)

    # camera1.open_camera_stream()
