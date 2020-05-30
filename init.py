import pygame
import os
import time
import pygetwindow as gw

print(gw.getAllTitles())

import pyautogui
import numpy as np
import keyboard
from directkeys import PressKey, DIK_U, DIK_9, DIK_2, DIK_1 , DIK_0

box_9 = (1100, 725)
hp_bar = (180, 80)
window_pos = (700, 0)

title = 'MapleHome'

maple_story = gw.getWindowsWithTitle(title)[0]

maple_story.activate()
time.sleep(2)

for i in range(10):
    pyautogui.press("ctrlleft")
    time.sleep(1)

# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')

#
# pyautogui.moveTo(box_9[0], box_9[1])
# pyautogui.moveTo(box_9[0], box_9[1])
# pyautogui.moveTo(window_pos[0], window_pos[1])
# pyautogui.moveTo(window_pos[0], window_pos[1])
#
# pyautogui.moveTo(window_pos[0], window_pos[1])
#
# pyautogui.rightClick()




