# from __future__ import print_function
from pywinauto.keyboard import send_keys
from pywinauto import mouse
from twilio.rest import Client
import time
from dateutil import tz
from datetime import datetime
import numpy as np
import cv2, win32gui, time, math, win32con, win32ui, win32api
from PIL import ImageGrab, Image
# key_codes: {<Name  Appear>: <Key Code to Send>}
key_codes = {'Insert': '{VK_INSERT}',
             'Delete': '{VK_DELETE}',
             'Home': '{VK_HOME}',
             'End': '{VK_END}',
             'Shift': '{VK_SHIFT}',
             'Control': '{VK_CONTROL}',
             'PageUp': '{PGUP}',
             'PageDown': '{PGDN}',
             'A': 'a',
             'B': 'b',
             'Z': 'z',
             ',': ',',
             'V': 'v'
             }

# Random helper functions
def toggle(boolean_value):
    if boolean_value == 1:
        boolean_value = 0
    else:
        boolean_value = 1
    return boolean_value

# General customized functions
def drink_mana(assign_slot):
    send_keys(assign_slot)

def drink_hp(assign_slot):
    send_keys(assign_slot)

def auto_attack(assign_slot):
    send_keys(assign_slot)

def pickup(assign_slot):
    send_keys('{} down'.format(assign_slot))
    send_keys('{} up'.format(assign_slot))

def buff(key_code):
    send_keys(key_code)

def feed_pet(assign_slot):
    send_keys(assign_slot)

def send_text_to_maplestory(message):
    send_keys('{ENTER}')
    time.sleep(0.5)
    send_keys(message)
    time.sleep(2)
    send_keys('{ENTER}')

def get_time():
    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    utc = datetime.utcnow()

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)

    # return central.strftime('%m/%d/%Y %H:%M:%S %Z')
    return central.strftime('%m/%d/%Y %H:%M:%S')

# Skyler's setting functions
def drink_mana():
    send_keys("{PGUP}")

def drink_hp():
    send_keys("{PGDN}")

def auto_attack():
    send_keys('{VK_CONTROL}')

def move_left_mage():
    # send_keys('+{LEFT}')
    send_keys('{RIGHT up}')
    send_keys('{LEFT up}')
    send_keys('{UP up}')

    send_keys('{LEFT down}')
    send_keys('{VK_SHIFT down}')
    send_keys('{VK_SHIFT up}')
    send_keys('{LEFT up}')

def move_right_mage():
    send_keys('{RIGHT up}')
    send_keys('{LEFT up}')
    send_keys('{UP up}')

    send_keys('{RIGHT down}')
    send_keys('{VK_SHIFT down}')
    send_keys('{VK_SHIFT up}')
    send_keys('{RIGHT up}')

def move_up_mage():
    send_keys('{RIGHT up}')
    send_keys('{LEFT up}')
    send_keys('{UP up}')

    send_keys('{UP down}')
    send_keys('{VK_SHIFT down}')
    send_keys('{VK_SHIFT up}')
    send_keys('{UP up}')

def pickup():
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')

def reset_minimap():
    send_keys('{m down}')
    send_keys('{m up}')

def sell_equipment(resOption):
    if resOption == 0: #1024x768
        mouse.double_click(button="left", coords=(477, 434))
    elif resOption == 1: #1280x768
        mouse.double_click(button="left", coords=(465, 435))
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    return

def exchange_giftbox():
    send_keys("{VK_SPACE}")
    time.sleep(0.5)
    send_keys("{VK_DOWN}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    send_keys("{RIGHT}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    send_keys("{ENTER}")

def exchange_regular_gac():
    send_keys("{VK_SPACE}")
    time.sleep(0.5)
    send_keys("{DOWN}")
    time.sleep(0.5)
    send_keys("{ENTER}")

def exchange_maple_coins_monstercarnival():
    send_keys("{VK_SPACE}")
    time.sleep(0.5)
    send_keys("{DOWN}")
    time.sleep(0.5)
    send_keys("{DOWN}")
    time.sleep(0.5)
    send_keys("{DOWN}")
    time.sleep(0.5)
    send_keys("{DOWN}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    send_keys("{RIGHT}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    time.sleep(0.5)
    send_keys("{ENTER}")
    return

def send_sms(message_to_send, phone_number):
    # Need to store it somewhere else
    account = "ACbbe9514e4619e8c9af58b344ba886df6"
    token = "a1b9b4b9d387cf79a0945f6be5314160"
    # Need to store it somewhere else
    client = Client(account, token)
    message = client.messages.create(to="+{}".format(phone_number), from_="+12058399940",
                                     body=message_to_send)
    return

def findHP():
    resOption = 0
    windows = ['MapleLegends (May 23 2020)', 'Nine Dragons', 'MapleHome', 'MapleStory']
    windowName = windows[3]
    hwndMain = win32gui.FindWindow(None, windowName)
    hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

    window_length_x = [1024, 1280]  # Resolution
    window_height_y = [768, 960]  # Resolution
    win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)

    # Minimap player marker original BGR: 136, 255, 255
    lower_red = np.array([0, 0, 130])  # B G R
    upper_red = np.array([5, 5, 256])
    lower_blue = np.array([100, 60, 0])  # B G R
    upper_blue = np.array([256, 190, 6])
    lower_grey = np.array([170, 170, 170])  # B G R
    upper_grey = np.array([192, 192, 192])


    bbox = (int(window_length_x[resOption]/4),
            int(window_height_y[resOption]/1.03),
            int(window_length_x[resOption]/1.82),
            window_height_y[resOption])

    im = ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img", im_np)

    # cv2.imwrite('HP_MP.jpg', im_np)
    mask_grey = cv2.inRange(im_np, lower_grey, upper_grey)
    mask_red = cv2.inRange(im_np, lower_red, upper_red)
    mask_blue = cv2.inRange(im_np, lower_blue, upper_blue)
    # for i in range(len(mask)):
    #     if 255 in mask[i]:
    #         print(i)

    # print(mask_red)
    cv2.imshow("Mask Grey", mask_grey)
    cv2.imshow("Mask Blue", mask_blue)
    cv2.imshow("Mask Red", mask_red)
    cv2.waitKey()
    td_grey = np.transpose(np.where(mask_grey > 0)).tolist()
    td_red = np.transpose(np.where(mask_red > 0)).tolist()
    td_blue = np.transpose(np.where(mask_blue > 0)).tolist()

    print(max(td_grey)[1] - min(td_grey)[1])
    print(max(td_red)[1] - min(td_red)[1])
    print(max(td_blue)[1] - min(td_blue)[1])

    # [y, x]

    # if len(td) > 0:
    #     x_list = [x[1] for x in td]
    #     y_list = [x[0] for x in td]
    #     avg_x = int(sum(x_list) / len(x_list))
    #     avg_y = int(sum(y_list) / len(y_list))
    #     return avg_x, avg_y
    #     # print((avg_x, avg_y))

    return 0


if __name__ == '__main__':
    # send_sms("Test message...", 14699695979)
    while True:
        # x, y = win32api.GetCursorPos()
        # print((x, y))
        sell_equipment(1)
    exit(0)