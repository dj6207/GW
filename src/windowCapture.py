import win32gui, win32ui, win32con
import numpy as np

class WinCapture:
    width = 0
    height = 0
    window = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    def __init__(self, window_name=None):
        # capture entire window if window name is not found or is none
        if window_name is None:
            self.window = win32gui.GetDesktopWindow()
        else:
            self.window = win32gui.FindWindow(None, window_name)
            if not self.window:
                print("Window not found, using desktop capture")
                self.window = win32gui.GetDesktopWindow()
        # window size
        window_rect = win32gui.GetWindowRect(self.window)
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]

    def get_frame(self):
        # get window image data
        window_dc = win32gui.GetWindowDC(self.window)
        dc = win32ui.CreateDCFromHandle(window_dc)
        # If create compatable dc failed that means the window does not exist or is currently minimized
        compatible_dc = dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc, self.width, self.height)
        compatible_dc.SelectObject(bitmap)
        compatible_dc.BitBlt((0, 0), (self.width, self.height), dc, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = bitmap.GetBitmapBits(True)
        image = np.fromstring(signedIntsArray, dtype='uint8')
        image.shape = (self.height, self.width, 4)

        # free resources
        dc.DeleteDC()
        compatible_dc.DeleteDC()
        win32gui.ReleaseDC(self.window, window_dc)
        win32gui.DeleteObject(bitmap.GetHandle())

        image = image[...,:3]
        image = np.ascontiguousarray(image)
        return image