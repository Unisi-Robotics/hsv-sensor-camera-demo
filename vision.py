import cv2 as cv
import numpy as np
import v4l2
import fcntl


class Camera:

    def __init__(self, devices, name, on_frame=True, lower_val=None, upper_val=None):

        if lower_val is None or upper_val is None:
            self.lower_val = [110, 150, 20]
            self.upper_val = [120, 255, 255]

        else:
            self.lower_val = lower_val
            self.upper_val = upper_val

        self.devices = devices
        self.cam = f'/dev/video{str(self.devices)}'
        self.cam_file = open(f'/dev/video{str(self.devices)}', 'r')
        self.name = name
        self.on_frame = on_frame

        if on_frame:
            self.cap = cv.VideoCapture(self.cam)

    def set_lowerHSV(self, lower):
        self.lower_val[0] = lower[0]
        self.lower_val[1] = lower[1]
        self.lower_val[2] = lower[2]

    def set_upperHSV(self, upper):
        self.upper_val[0] = upper[0]
        self.upper_val[1] = upper[1]
        self.upper_val[2] = upper[2]

    def HSV_calibration(self, frame):
        self.upper_val = np.asarray(self.upper_val)
        self.lower_val = np.asarray(self.lower_val)

        frame = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
        frame = cv.inRange(frame, self.lower_val, self.upper_val)

        return frame

    def get_frame(self):
        frame = []

        try:
            _, frame = self.cap.read()

        except Exception as e:
            print('get frame', e)

        return frame

    def set_capture(self, on_frame=True):
        self.on_frame = on_frame

        if on_frame:
            self.cam = cv.VideoCapture(self.cam)

        else:
            self.cam.release()

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
        Dark Blue: lower: [110, 150, 20], upper: [120, 255, 255]

    """

    pass

    # Testing Camera
    # Comment terlebih dahulu sebelum bagian buat objek camera1 dan camera2 di atas
    # camera3 = Camera(2, 'Camera:1', lower_val=[
    #                  110, 150, 20], upper_val=[120, 255, 255])

    # while True:
    #     frame = camera3.get_frame()
    #     frame = camera3.HSV_calibration(frame)

    #     cv.imshow('Test Camera', frame)

    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break
