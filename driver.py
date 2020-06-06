import time
from datetime import datetime
from basic_functions import *
import pygetwindow as gw
from dateutil import tz
import PIL.ImageGrab
import win32gui
import win32con
import win32api
import numpy as np
from tkinter import *
import tkinter.ttk
import threading
from random import *

# GLOBAL SETTINGS
windows = ['MapleLegends (May 23 2020)', 'Nine Dragons', 'MapleHome', 'MapleStory']
windowName = windows[3]

window_length_x = [1024, 1280] # This will be modified at real-time
window_height_y = [768, 960] # This should be modified at real-time

resOption = 0 # 0 for 1024x768 | 1 for 1280x960

from_mp_global = 50 # percent
to_mp_global = 80 # percent
from_hp_global = 70 # percent
to_hp_global = 80 # percent
# GLOBAL SETTINGS

# Random Vars (to make things more random and trick lie detector)

hp_percent_random = 80
mp_percent_random = 80
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

    # return central.strftime('%m/%d/%Y %H:%M:%S %Z')
    return central.strftime('%m/%d/%Y %H:%M:%S')


def get_window_image(window_name):
    hwndMain = win32gui.FindWindow(None, window_name)
    hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

    win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)
    bbox = win32gui.GetWindowRect(hwndMain)

    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.BGR2GRAY)

    # cv2.imshow("Window image", im_np)
    # cv2.waitKey()

def botting():
    return

def lie_detector():
    return False

def main(windowName):
    global hp_percent_random, \
        mp_percent_random, \
        from_mp_global, \
        to_mp_global, \
        from_hp_global, \
        to_hp_global
    global buff_delay, \
        random_buff_delay
    # Buff all when start
    buff_0()
    time.sleep(0.2)
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
            if auto_hp(hp_percent_random, resOption):
                hp_percent_random = randint(from_hp_global, to_hp_global)
                # print("HP: {} {}".format(from_hp_global, to_hp_global))

        if is_auto_mp == 1:
            # print("MP: {}".format(mp_percent_random))
            if auto_mp(mp_percent_random, resOption):
                mp_percent_random = randint(from_mp_global, to_mp_global)

        if is_auto_attack == 1:
            auto_attack()

        if is_auto_pickup == 1:
            pickup()

def ui():
    global maple_story
    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup,\
        resOption
    global to_mp_global, \
        to_hp_global, \
        from_mp_global, \
        from_hp_global

    root = Tk()

    # UI Vars

    is_auto_hp = IntVar()
    is_auto_hp.set(0)
    is_auto_mp = IntVar()
    is_auto_mp.set(0)
    is_auto_attack = IntVar()
    is_auto_attack.set(0)
    is_auto_pickup = IntVar()
    is_auto_pickup.set(0)

    fromHpEntry = StringVar()
    fromHpEntry.set(str(from_hp_global))
    toHpEntry = StringVar()
    toHpEntry.set(str(to_hp_global))

    fromMpEntry = StringVar()
    fromMpEntry.set(str(from_mp_global))
    toMpEntry = StringVar()
    toMpEntry.set(str(to_mp_global))

    time_buff_0_input = StringVar()
    time_buff_1_input = StringVar()
    time_buff_2_input = StringVar()
    time_buff_3_input = StringVar()
    time_buff_4_input = StringVar()

    tkResOption = IntVar()
    tkResOption.set(0)  # 0 for 1024x768 | 1 for 1280x960

    # UI Vars

    root.title("MapleStory Bot")

    is_auto_hp = IntVar(value=0)
    is_auto_mp = IntVar(value=0)
    is_auto_attack = IntVar(value=0)
    is_auto_pickup = IntVar(value=0)


    def change_auto_mp_state():
        global is_auto_mp
        is_auto_mp = not is_auto_mp
        # print("Auto MP state", is_auto_mp)
        maple_story.activate()

    def change_auto_hp_state():
        global is_auto_hp
        is_auto_hp = not is_auto_hp
        # print("Auto HP state", is_auto_hp)
        maple_story.activate()


    def change_auto_attack_state():
        global is_auto_attack
        is_auto_attack = not is_auto_attack
        # print("Auto attack state", is_auto_attack)
        maple_story.activate()

    def change_auto_pickup_state():
        global is_auto_pickup
        is_auto_pickup = not is_auto_pickup
        # print("Auto pick up state", is_auto_pickup)
        maple_story.activate()

    def toggle_resolution():
        global resOption, windowName
        resOption = tkResOption.get()
        hwndMain = win32gui.FindWindow(None, windowName)
        win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)
        maple_story.activate()

    def setHpRange():
        global from_hp_global, to_hp_global
        try:
            from_hp_global = int(fromHpEntry.get())
            to_hp_global = int(toHpEntry.get())
            # print("HP here: ", from_hp_global , to_hp_global)

        except:
            from_hp_global = 0
            to_hp_global = 0
            print("Invalid input HP")

    def setMpRange():
        global from_mp_global, to_mp_global
        try:
            from_mp_global = int(fromMpEntry.get())
            to_mp_global = int(toMpEntry.get())
            # print("MP here: ", from_mp_global , to_mp_global)
        except:
            from_mp_global = 0
            to_mp_global = 0
            print("Invalid input MP")

    canvas_width = 100
    canvas_height = 10

    root.geometry('{}x{}'.format(450, 250))

    # Auto HP Row
    row = 0
    Checkbutton(root,
                text='Auto HP',
                command=change_auto_hp_state,
                variable=is_auto_hp,
                ).grid(row=row)

    fromHpLabel = Label(root,
                        text="From:").grid(column=4,
                                           row=row)
    Entry(root,
          textvariable=fromHpEntry).grid(column=5,
                                         row=row)

    toHpLabel = Label(root,
                      text="To:").grid(column=8,
                                       row=row)
    Entry(root,
          textvariable=toHpEntry).grid(column=9,
                                       row=row)

    Button(root, text='Set',
           command=setHpRange).grid(column=10,
                                    row=row)
    # line
    row += 1
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height)
    w.grid(row=row)

    y = int(canvas_height / 2)
    w.create_line(0, y, canvas_width, y, fill="#476042")
    #Auto HP Row ---

    #Auto MP Row
    row += 1
    Checkbutton(root,
                text='Auto MP',
                command=change_auto_mp_state,
                variable=is_auto_mp,
                ).grid(column=0, row=row)

    fromMpLabel = Label(root,
                        text="From:").grid(column=4,
                                           row=row)
    Entry(root,
          textvariable=fromMpEntry).grid(column=5,
                                         row=row)

    toMpLabel = Label(root,
                      text="To:").grid(column=8,
                                       row=row)
    Entry(root,
          textvariable=toMpEntry).grid(column=9,
                                       row=row)

    Button(root, text='Set',
           command=setMpRange).grid(column=10,
                                    row=row)

    # line
    row += 1
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height)
    w.grid(row=row)

    y = int(canvas_height / 2)
    w.create_line(0, y, canvas_width, y, fill="#476042")
    #Auto MP Row ---

    #Auto Attack Row
    row += 1
    Checkbutton(root,
                text='Auto Attack',
                command=change_auto_attack_state,
                variable=is_auto_attack,
                ).grid(row=row, sticky=W)

    #Auto Pickup Row
    row += 1
    Checkbutton(root,
                text='Auto Pickup',
                command=change_auto_pickup_state,
                variable=is_auto_pickup,
                ).grid(row=row, sticky=W)

    #1024x768 resolution
    Radiobutton(root,
                text="1024x768",
                command=toggle_resolution,
                variable=tkResOption,
                value=0).grid(sticky=W)

    #1280x920 resolution
    Radiobutton(root,
                text="1280x920",
                command=toggle_resolution,
                variable=tkResOption,
                value=1).grid(sticky=W)


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

    # get_window_image(windowName)

    print("Connected!")
    time.sleep(2)

    threading.Thread(target=ui).start()
    threading.Thread(target=main(windowName)).start()

    # write_walls()    # <-to uncomment replace first #



