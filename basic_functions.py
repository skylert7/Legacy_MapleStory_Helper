from telecast import *
from datetime import datetime
from random import randint
import PIL.ImageGrab
import cv2
import numpy as np

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

def move_left():
    send_keys('{LEFT down}')
    send_keys('{LEFT up}')

def move_right():
    send_keys('{RIGHT down}')
    send_keys('{RIGHT up}')

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

def buff_0():
    send_keys('{VK_HOME down}')
    send_keys('{VK_HOME up}')

def buff_1():
    send_keys('{VK_DELETE down}')
    send_keys('{VK_DELETE up}')

def buff_2():
    send_keys('{VK_INSERT down}')
    send_keys('{VK_INSERT up}')

def buff_3():
    send_keys('{VK_END down}')
    send_keys('{VK_END up}')

def move_and_pickup():
    # pick up from the right
    for i in range(4):
        send_keys('{RIGHT down}')
        pickup()
        pickup()
        pickup()
        send_keys('{RIGHT up}')


    # pick up from the left
    for i in range(6):
        send_keys('{LEFT down}')
        pickup()
        pickup()
        pickup()
        pickup()
        pickup()
        send_keys('{LEFT up}')

    # go back to center
    for i in range(4):
        send_keys('{RIGHT down}')
        pickup()
        pickup()
        pickup()
        pickup()
        pickup()
        send_keys('{RIGHT up}')

def auto_hp(window_name, percent):
    # Maple Legends
    x1 = 224
    x2 = 320
    y1 = 745
    y2 = 765

    bbox = (x1, y1, x2, y2)
    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # pick an array to analyze current hp and full hp
    im_np[10]
    # return unique values and count of each unique value
    unique, counts = np.unique(im_np[10], return_counts=True)

    if (counts[0] / (x2 - x1)) * 100 < percent:
        print("Percent HP: ", counts[0] / (x2 - x1) * 100)
        drink_hp()
        # drink hp and delay for 1s
        time.sleep(0.5)
        return

    return

def auto_mp(window_name, percent):
    # Maple Legends
    x1 = 333
    x2 = 430
    y1 = 750
    y2 = 765

    bbox = (x1, y1, x2, y2)
    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    # pick an array to analyze current hp and full hp

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    item = 0

    for x in range(len(im_np[10])):
        if im_np[10][x] > 100:
            item = x
            break

    if item / (x2 - x1) * 100 < percent and item / (x2 - x1) * 100 != 0:
        print("Percent MP: ", item / (x2 - x1) * 100)
        drink_mana()
        # drink mana and delay for 1s
        time.sleep(0.5)
        return

    # cv2.imshow("image", im_np)
    # cv2.waitKey()
    return