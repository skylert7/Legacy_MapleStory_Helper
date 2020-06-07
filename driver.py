from datetime import datetime
from basic_functions import *
import pygetwindow as gw
from dateutil import tz
import win32gui
import win32con
import win32api
from tkinter import *
import threading
from random import *
import keyboard
import tkinter as tk

# GLOBAL SETTINGS
windows = ['MapleLegends (May 23 2020)', 'Nine Dragons', 'MapleHome', 'MapleStory']
windowName = windows[3]

window_length_x = [1024, 1280] # This will be modified at real-time
window_height_y = [768, 960] # This should be modified at real-time

resOption = 0 # 0 for 1024x768 | 1 for 1280x960

is_auto_attack = 0
is_auto_mp = 0
is_auto_hp = 0
is_auto_pickup = 0

from_mp_global = 50 # percent
to_mp_global = 80 # percent
from_hp_global = 70 # percent
to_hp_global = 80 # percent

buff_delay = [200, 200, 600, 0]
buff_state = [0] * len(buff_delay)
key_options = ["String"] * len(buff_delay)
# GLOBAL SETTINGS

# Random Vars (to make things more random and trick lie detector)

hp_percent_random = 80
mp_percent_random = 80
random_buff_delay = [0] * len(buff_delay)
for i in range(len(buff_delay)):
    random_buff_delay[i] = randint(buff_delay[i] // 4, buff_delay[i]//2)

# Random Vars

# bbox (left_x, top_y, right_x, bottom_y)

def toggle(aState):
    return not aState

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

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

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
        random_buff_delay,\
        key_options

    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup

    OPTIONS = list(key_codes.keys())

    # Copy over key codes from OPTIONS to key_options for global use
    for index in range(len(buff_delay)):
        key_options[index] = OPTIONS[index]

    # Buff all when start
    for index in range(len(buff_delay)):
        buff(key_codes[OPTIONS[index]])
        time.sleep(2)

    time_at_buff = [datetime.utcnow()] * len(buff_delay)
    while True:
        # Buffs
        for index in range(len(buff_delay)):
            if buff_state[index]:
                if (datetime.utcnow() - time_at_buff[index]).total_seconds() > random_buff_delay[index]:
                    buff(key_codes[key_options[index]])
                    buff(key_codes[key_options[index]])
                    print("Buff %d at: " % (index + 1), get_time())
                    time_at_buff[index] = datetime.utcnow()
                    random_buff_delay[index] = randint(int(buff_delay[index]) // 4, int(buff_delay[index])//2)

        # AutoHP
        if is_auto_hp == 1:
            if auto_hp(hp_percent_random, resOption):
                hp_percent_random = randint(from_hp_global, to_hp_global)
                # print("HP: {} {}".format(from_hp_global, to_hp_global))

        # AutoMP
        if is_auto_mp == 1:
            # print("MP: {}".format(mp_percent_random))
            if auto_mp(mp_percent_random, resOption):
                mp_percent_random = randint(from_mp_global, to_mp_global)

        # AutoAttack
        if is_auto_attack == 1:
            auto_attack()

        # AutoPickUp
        if is_auto_pickup == 1:
            pickup()

def ui():
    global maple_story
    # Global for True/False var
    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup,\
        resOption, \
        buff_state
    # Global for string/int var
    global to_mp_global, \
        to_hp_global, \
        from_mp_global, \
        from_hp_global, \
        buff_delay, \
        key_options

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

    buff_reset_time = list()
    buff_state_ui = list()

    for index in range(len(buff_delay)):
        varTime = StringVar()
        varTime.set(str(buff_delay[index]))
        varState = IntVar()
        varState.set(0)
        buff_reset_time.append(varTime)
        buff_state_ui.append(varState)

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
        print("Auto attack state", is_auto_attack)
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

    def re_assign_time_and_key_buff(num):
        for var in range(len(var_list)):
            key_options[var] = var_list[var].get()
            buff_delay[var] = buff_reset_time[var].get()
            buff_state[var] = buff_state_ui[var].get()

    # Some variables to use
    canvas_width = 100
    canvas_height = 10
    OPTIONS = list(key_codes.keys())
    # Some variables to use

    # default panel size
    root.geometry('{}x{}'.format(450, 500))

    # Auto HP Row
    row = 0
    Checkbutton(root,
                text='Auto HP',
                command=change_auto_hp_state,
                variable=is_auto_hp,
                ).grid(row=row,
                       column=0)

    fromHpLabel = Label(root,
                        text="From:"
                        ).grid(column=1,
                               row=row)
    Entry(root,
          textvariable=fromHpEntry,
          width=8).grid(column=2,
                        row=row)

    toHpLabel = Label(root,
                      text="To:"
                      ).grid(column=3,
                             row=row)
    Entry(root,
          textvariable=toHpEntry,
          width=8
          ).grid(column=4,
                 row=row)

    Button(root,
           text='Set',
           command=setHpRange
           ).grid(column=5,
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
                        text="From:"
                        ).grid(column=1,
                               row=row)
    Entry(root,
          textvariable=fromMpEntry,
          width=8
          ).grid(column=2,
                 row=row)

    toMpLabel = Label(root,
                      text="To:"
                      ).grid(column=3,
                             row=row)
    Entry(root,
          textvariable=toMpEntry,
          width=8
          ).grid(column=4,
                 row=row)

    Button(root,
           text='Set',
           command=setMpRange
           ).grid(column=5,
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
                ).grid(row=row, column=0, sticky=W)

    #Auto Pickup Row
    row += 1
    Checkbutton(root,
                text='Auto Pickup',
                command=change_auto_pickup_state,
                variable=is_auto_pickup,
                ).grid(row=row, column=0, sticky=W)

    #1024x768 resolution
    row += 1
    Radiobutton(root,
                text="1024x768",
                command=toggle_resolution,
                variable=tkResOption,
                value=0
                ).grid(row=row,
                       column=0,
                       sticky=W)

    #1280x920 resolution
    row += 1
    Radiobutton(root,
                text="1280x920",
                command=toggle_resolution,
                variable=tkResOption,
                value=1
                ).grid(row=row,
                       column=0,
                       sticky=W)

    #Buff Rows
    var_list = list()
    for pos in range(4):
        row += 1
        Checkbutton(root,
                    text='Buff {}'.format(pos),
                    variable=buff_state_ui[pos],
                    command=lambda x=index: re_assign_time_and_key_buff(x)
                    ).grid(column=0,
                           row=row)
        Label(root,
              text="Reset Time:").grid(column=1,
                                       row=row)
        Entry(root,
              textvariable=buff_reset_time[pos],
              width=8
              ).grid(column=2,
                     row=row)

        Label(root,
              text="Key:"
              ).grid(column=3,
                     row=row)

        #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
        variable = StringVar(root)
        variable.set(OPTIONS[pos])  # default value
        var_list.append(variable)
        optionMenu = OptionMenu(root, var_list[pos], *OPTIONS)
        optionMenu.grid(row=row,
                        column=4)
        #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter

        Button(root,
               text='Set',
               command=lambda x=index: re_assign_time_and_key_buff(x)
               ).grid(column=5,
                      row=row)

        # line
        row += 1
        w = Canvas(root,
                   width=canvas_width,
                   height=canvas_height)
        w.grid(row=row)

        y = int(canvas_height / 2)
        w.create_line(0, y, canvas_width, y, fill="#476042")
    #Buff Rows ---


    #Notes (Text)
    row += 1
    note_text = Label(root, text="Notes:\nF3 to toggle Auto Attack.\nF4 to toggle Auto Pickup.")
    note_text.grid(row=row, sticky=W)


    root.mainloop()

    return

def on_press_reaction(event):
    #https://stackoverflow.com/questions/47184374/increase-just-by-one-when-a-key-is-pressed/47184663
    global is_auto_attack, is_auto_pickup
    if event.name == 'f3':
        is_auto_attack = not is_auto_attack
        print("Auto attack state %s" % is_auto_attack)
    if event.name == 'f4':
        is_auto_pickup = not is_auto_pickup
        print("Auto pick up state %s" % is_auto_pickup)

if __name__ == '__main__':
    keyboard.on_press(on_press_reaction)
    try:

        maple_story = gw.getWindowsWithTitle(windowName)[0] # Get window by name

    except:

        print("Can't find MapleStory Client... Exiting")
        exit(0)

    maple_story.activate() # Bring window on top

    get_window_image(windowName)

    print("Connected!")
    time.sleep(1)

    threading.Thread(target=ui).start()
    threading.Thread(target=main(windowName)).start()

    # write_walls()    # <-to uncomment replace first #





