import time
from datetime import datetime
from telecast import *
from basic_functions import *
import pygetwindow as gw
from dateutil import tz
import PIL.ImageGrab
import win32gui
import numpy as np
from tkinter import *
import threading
from random import *

# GLOBAL SETTINGS
windows = ['MapleLegends (May 23 2020)', 'Nine Dragons', 'MapleHome', 'MapleStory']
windowName = windows[3]
window_length_x = 1024 # This will be modified at real-time
window_height_y = 768 # This should be modified at real-time

hp_percent_to_drink_potion = 50 # percent
mp_percent_to_drink_potion = 70 # percent
# GLOBAL SETTINGS

# UI Vars

is_auto_hp = IntVar
is_auto_mp = IntVar
is_auto_attack = IntVar
is_auto_pickup = IntVar

time_buff_0_input = StringVar
time_buff_1_input = StringVar
time_buff_2_input = StringVar
time_buff_3_input = StringVar
time_buff_4_input = StringVar

# UI Vars

# Random Vars (to make things more random and trick lie detector)

hp_pecent_random = randint(hp_percent_to_drink_potion // 2, hp_percent_to_drink_potion)
mp_percent_random = randint(mp_percent_to_drink_potion // 2, mp_percent_to_drink_potion)
buff_delay = [600, 90, 0, 0, 0]
random_buff_delay = [0, 0, 0, 0]
random_buff_delay[0] = randint(buff_delay[0] // 2, buff_delay[0])
random_buff_delay[1] = randint(buff_delay[1] // 2, buff_delay[1])

# Random Vars

# bbox (left_x, top_y, right_x, bottom_y)

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

    return central.strftime('%m/%d/%Y %H:%M:%S %Z')

def get_window_image(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    win32gui.MoveWindow(hwnd, 0, 0, window_length_x, window_height_y, True)
    bbox = win32gui.GetWindowRect(hwnd)

    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

def botting():
    return

def lie_detector():
    return False

def get_left_mob():
    return

def get_right_mob():
    return

def main(windowName):
    global hp_pecent_random, \
        mp_percent_random, \
        hp_percent_to_drink_potion, \
        mp_percent_to_drink_potion
    global buff_delay, \
        random_buff_delay
    count = 0
    # Buff all when start
    buff_0()
    buff_1()

    time_at_buff = [datetime.utcnow()] * 4
    while True:
        if (datetime.utcnow() - time_at_buff[0]).total_seconds() > random_buff_delay[0]:
            buff_0()
            buff_0()
            print("Buff 0 at: ", get_time())
            time_at_buff[0] = datetime.utcnow()
            random_buff_delay[0] = randint(buff_delay[0] // 2, buff_delay[0])

        if (datetime.utcnow() - time_at_buff[1]).total_seconds() > random_buff_delay[1]:
            buff_1()
            buff_1()
            print("Buff 1 at: ", get_time())
            time_at_buff[1] = datetime.utcnow()
            random_buff_delay[1] = randint(buff_delay[1] // 2, buff_delay[1])

        # if (datetime.utcnow() - time_at_buff).total_seconds() > buff_delay[0]:
        #     buff_0()
        #     buff_0()
        #     print("Buff at: ", get_time())
        #     time_at_buff = datetime.utcnow()
        #
        # if (datetime.utcnow() - time_at_buff).total_seconds() > buff_delay[0]:
        #     buff_0()
        #     buff_0()
        #     print("Buff at: ", get_time())
        #     time_at_buff = datetime.utcnow()

        if is_auto_hp == 1:
            auto_hp(windowName, hp_pecent_random)
            hp_pecent_random = randint(hp_percent_to_drink_potion // 2, hp_percent_to_drink_potion)

        if is_auto_mp == 1:
            auto_mp(windowName, mp_percent_random)
            mp_percent_random = randint(mp_percent_to_drink_potion // 2, mp_percent_to_drink_potion)

        if is_auto_attack == 1:
            auto_attack()

        if is_auto_pickup == 1:
            pickup()

        # if count % 10 == 0:
        #     move_left()
        # if count % 20 == 0:
        #     move_right()
        # if count == 400:
        #     print("Picking things up..")
        #     move_and_pickup()
        #     count = 0
        # #     # time.sleep(randint(0, 10))
        # count = count + 1




def ui():
    global maple_story
    global is_auto_attack, is_auto_mp, is_auto_hp, is_auto_pickup
    root = Tk()
    root.title("MapleStory Bot")

    is_auto_hp = IntVar(value=0)
    is_auto_mp = IntVar(value=0)
    is_auto_attack = IntVar(value=0)
    is_auto_pickup = IntVar(value=0)


    def change_auto_mp_state():
        global is_auto_mp
        is_auto_mp = not is_auto_mp
        print("Auto MP state", is_auto_mp)
        maple_story.activate()

    def change_auto_hp_state():
        global is_auto_hp
        is_auto_hp = not is_auto_hp
        print("Auto HP state", is_auto_hp)
        maple_story.activate()


    def change_auto_attack_state():
        global is_auto_attack
        is_auto_attack = not is_auto_attack
        print("Auto attack state", is_auto_attack)
        maple_story.activate()

    def change_auto_pickup_state():
        global is_auto_pickup
        is_auto_pickup = not is_auto_pickup
        print("Auto pick up state", is_auto_pickup)
        maple_story.activate()

    root.geometry('350x200')

    row = 0
    Checkbutton(root,
                text='Auto HP',
                command=change_auto_hp_state,
                variable=is_auto_hp,
                ).grid(row=row)

    row += 1
    Checkbutton(root,
                text='Auto MP',
                command=change_auto_mp_state,
                variable=is_auto_mp,
                ).grid(row=row)


    row += 1
    Checkbutton(root,
                text='Auto Attack',
                command=change_auto_attack_state,
                variable=is_auto_attack,
                ).grid(row=row, sticky=W)

    row += 1
    Checkbutton(root,
                text='Auto Pickup',
                command=change_auto_pickup_state,
                variable=is_auto_pickup,
                ).grid(row=row, sticky=W)

    root.mainloop()

    return

def testLoop():
    for x  in range(2000):
        print(x)

def testLoop1():
    for x  in range(400):
        print(x)

if __name__ == '__main__':
    try:

        maple_story = gw.getWindowsWithTitle(windowName)[0] # Get window by name

    except:

        print("Can't find MapleLegends... Exiting")
        exit(0)

    maple_story.activate() # Bring window on top

    get_window_image(windowName)

    print("Connected!")
    time.sleep(2)

    threading.Thread(target=ui).start()
    threading.Thread(target=main(windowName)).start()


    # write_walls()    # <-to uncomment replace first #



