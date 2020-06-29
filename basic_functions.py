from import_standalone import *
from pywinauto.keyboard import send_keys
from PIL import ImageGrab
import numpy as np
import cv2, win32gui, time, math, win32con, win32ui
from twilio.rest import Client



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

def send_sms(message_to_send, phone_number):
    # Need to store it somewhere else
    account = "ACbbe9514e4619e8c9af58b344ba886df6"
    token = "a1b9b4b9d387cf79a0945f6be5314160"
    # Need to store it somewhere else
    client = Client(account, token)
    message = client.messages.create(to="+{}".format(phone_number), from_="+12058399940",
                                     body=message_to_send)
    return

if __name__ == '__main__':

    exit(0)