from __future__ import print_function

from import_standalone import *
from pywinauto.keyboard import send_keys
from PIL import ImageGrab
import numpy as np
import cv2, win32gui, time, math, win32con, win32ui
from twilio.rest import Client
import sys
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range


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

# General customized functions
def drink_mana(assign_slot):
    send_keys(assign_slot)

def auto_attack(assign_slot):
    send_keys(assign_slot)

def pickup(assign_slot):
    send_keys('{} down'.format(assign_slot))
    send_keys('{} up'.format(assign_slot))

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

def buff(key_code):
    send_keys(key_code)

def auto_hp(percent, resOption):
    '''
    choices: 1024 x 768 (0) OR 1280 x 960 (1)
    '''

    x_start = [285, 356]
    x_end = [412, 508]
    y_start = [744, 936]
    y_end = [762, 954]

    bbox = (x_start[resOption], y_start[resOption], x_end[resOption], y_end[resOption])

    im = ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # pick an array to analyze current hp and full hp
    # print("HP: ", im_np[10])
    # print("Auto HP. Random percent: {}. Res Option: {}".format(percent, resOption))
    # cv2.imshow("HP", im_np)
    # cv2.waitKey()

    # return unique values and count of each unique value
    unique, counts = np.unique(im_np[10], return_counts=True)

    if (counts[0] / (x_end[resOption] - x_start[resOption])) * 100 < percent:
        # print("Percent HP: ", counts[0] / (x_end[resOption] - x_start[resOption]) * 100)
        drink_hp()
        # drink hp and delay for .1s
        time.sleep(0.2)
        return True

    return False

def auto_mp(percent, resOption):
    '''
    choices: 1024 x 768 (0) OR 1280 x 960 (1)
    '''

    x_start = [424, 530]
    x_end = [551, 682]
    y_start = [744, 936]
    y_end = [762, 954]

    bbox = (x_start[resOption], y_start[resOption], x_end[resOption], y_end[resOption])

    im = ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    # pick an array to analyze current hp and full hp

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # print("MP: ", im_np[10])
    # print("Auto MP. Random percent: {}. Res Option: {}".format(percent, resOption))
    # cv2.imshow("MP", im_np)
    # cv2.waitKey()

    item = 0

    # 178 is empty - 1024x768
    # 134 is empty - 1280x960
    empty = [175, 130]
    for x in range(len(im_np[10])):
        if im_np[10][x] > empty[resOption]:
            item = x
            break

    if item / (x_end[resOption] - x_start[resOption]) * 100 < percent and \
            item / (x_end[resOption] - x_start[resOption]) * 100 != 0:
        # print("Percent MP: ", item / (x_end[resOption] - x_start[resOption]) * 100)
        drink_mana()
        # drink mana and delay for .1s
        time.sleep(0.2)
        return True

    return False

def reset_minimap():
    send_keys('{m down}')
    send_keys('{m up}')

def send_text_to_maplestory(message):
    send_keys('{ENTER}')
    time.sleep(0.5)
    send_keys(message)
    time.sleep(2)
    send_keys('{ENTER}')

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

def send_sms(message_to_send, phone_number):
    # Need to store it somewhere else
    account = "ACbbe9514e4619e8c9af58b344ba886df6"
    token = "a1b9b4b9d387cf79a0945f6be5314160"
    # Need to store it somewhere else
    client = Client(account, token)
    message = client.messages.create(to="+{}".format(phone_number), from_="+12058399940",
                                     body=message_to_send)
    return

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

def main():
    img = ImageGrab.grab(bbox=(0, 0, 1024/3, 768/3))
    img = np.array(img)
    # img = cv2.imread(im)
    squares = find_squares(img)
    print(squares)
    cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
    cv2.imshow('squares', img)
    ch = cv2.waitKey()
    if ch == 27:
        pass

    print('Done')

def findHP():
    resOption = 1
    windows = ['MapleLegends (May 23 2020)', 'Nine Dragons', 'MapleHome', 'MapleStory']
    windowName = windows[3]
    hwndMain = win32gui.FindWindow(None, windowName)
    hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

    window_length_x = [1024, 1280]  # Resolution
    window_height_y = [768, 960]  # Resolution
    win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)

    # Minimap player marker original BGR: 136, 255, 255
    lower_red = np.array([0, 0, 254])  # B G R
    upper_red = np.array([71, 99, 256])
    lower_blue = np.array([204, 0, 0])  # B G R
    upper_blue = np.array([256, 256, 51])
    lower_grey = np.array([170, 170, 170])  # B G R
    upper_grey = np.array([192, 192, 192])


    bbox = (int(window_length_x[resOption]/4),
            int(window_height_y[resOption]/1.05),
            int(window_length_x[resOption]/1.6),
            window_height_y[resOption])

    im = ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img", im_np)

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
    findHP()
    exit(0)