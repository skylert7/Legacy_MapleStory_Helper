import time
import win32gui

from PIL import ImageOps, Image, ImageGrab
from numpy import *
import time
import cv2
import win32gui


def get_window_info():
    # set window info
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info

def get_screen(x1, y1, x2, y2):
    box = (x1 + 8, y1 + 30, x2 - 8, y2)
    screen = ImageGrab.grab(box)
    img = array(screen.getdata(), dtype=uint8).reshape((screen.size[1], screen.size[0], 3))
    return img

window_info = get_window_info()

img = get_screen(
    window_info["x"],
    window_info["y"],
    window_info["x"] + window_info["width"],
    window_info["y"] + window_info["height"] - 190
)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

