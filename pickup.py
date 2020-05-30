import time
from datetime import datetime
from pywinauto import Application
from telecast import *
from multiprocessing import Process
from basic_functions import *
from threading import Thread
import pyautogui

while True:
    print(pyautogui.position())