from import_standalone import *
from screen_processing import *
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
is_move_left = 0
is_move_right = 0
is_keep_center = 0

from_mp_global = 50 # percent
to_mp_global = 80 # percent
from_hp_global = 70 # percent
to_hp_global = 80 # percent
attack_delay_global = 100 # milliseconds
buff_delay = [200, 200, 600, 0]
buff_state = [0] * len(buff_delay)
moveDelay = [1000, 1000]  # [left, right] in milliseconds

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

    im = ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("Window image", im_np)
    # cv2.waitKey()

def botting():
    try:
        static.update_image()
        x_minmap, y_minmap, w_minmap, h_minmap = static.get_minimap_rect()
        user_coor = static.find_player_minimap_marker(rect=[x_minmap, y_minmap, w_minmap, h_minmap])  # tuple
        # Ghost Ship 1024x768
        # Top Right: (139, 35)
        # Top Left: (15, 35)
        # Bottom Right: (125, 54)
        # Bottom Left: (15, 54)
        # middle_point = (139 - 15)//2
        middle_point = (125 - 15) // 2
        middle_area = [middle_point - 2,
                       middle_point + 2,
                       middle_point - 1,
                       middle_point + 1,
                       middle_point]
        # print(user_coor)
        # print(type(user_coor))

        if user_coor[0] in middle_area:
            # print("Middle")
            pass
        elif user_coor[0] > middle_point:  # char is on the right
            # print("Right")
            move_left_mage()
        elif user_coor[0] < middle_point:  # char is on the left
            # print("Left")
            move_right_mage()
    except:
        move_right_mage()
        move_left_mage()

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
        is_auto_pickup, \
        is_move_left, \
        is_move_right, \
        is_keep_center

    OPTIONS = list(key_codes.keys())

    # Screen Processing
    dx = MapleScreenCapturer()
    hwnd = dx.ms_get_screen_hwnd()
    rect = dx.ms_get_screen_rect(hwnd)

    static = StaticImageProcessor(dx)
    static.update_image()
    # Screen Processing

    # Copy over key codes from OPTIONS to key_options for global use
    for index in range(len(buff_delay)):
        key_options[index] = OPTIONS[index]

    # Buff all when start
    for index in range(len(buff_delay)):
        buff(key_codes[OPTIONS[index]])
        time.sleep(2)

    time_at_buff = [datetime.utcnow()] * len(buff_delay)
    time_at_move = [datetime.utcnow()] * len(moveDelay)
    time_at_attack = datetime.utcnow()
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
            if (datetime.utcnow() - time_at_attack).total_seconds() > (attack_delay_global / 1000):
                auto_attack()
                time_at_attack = datetime.utcnow()

        # AutoPickUp
        if is_auto_pickup == 1:
            pickup()

        if is_move_left == 1:
            if (datetime.utcnow() - time_at_move[0]).total_seconds() > (moveDelay[0] / 1000):
                move_left_mage()
                time_at_move[0] = datetime.utcnow()

        if is_move_right == 1:
            if (datetime.utcnow() - time_at_move[1]).total_seconds() > (moveDelay[1] / 1000):
                move_right_mage()
                time_at_move[1] = datetime.utcnow()

        # Move Around Map Horizontally
        if is_keep_center == 1:
            botting()

def ui():
    global maple_story
    # Global for True/False var
    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup,\
        is_keep_center, \
        resOption, \
        buff_state
    # Global for string/int var
    global to_mp_global, \
        to_hp_global, \
        from_mp_global, \
        from_hp_global, \
        attack_delay_global, \
        buff_delay, \
        key_options

    root = Tk()

    # UI Vars

    is_auto_hp = IntVar(value=int(is_auto_hp))
    is_auto_mp = IntVar(value=int(is_auto_mp))
    is_auto_attack = IntVar(value=int(is_auto_attack))
    is_auto_pickup = IntVar(value=int(is_auto_pickup))
    is_keep_center = IntVar(value=int(is_keep_center))

    fromHpEntry = StringVar()
    fromHpEntry.set(str(from_hp_global))
    toHpEntry = StringVar()
    toHpEntry.set(str(to_hp_global))

    fromMpEntry = StringVar()
    fromMpEntry.set(str(from_mp_global))
    toMpEntry = StringVar()
    toMpEntry.set(str(to_mp_global))

    attackDelayUI = StringVar()
    attackDelayUI.set(str(attack_delay_global))

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

    def change_keep_center():
        global is_keep_center
        is_keep_center = not is_keep_center
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

    def set_attack_delay():
        global attack_delay_global
        try:
            attack_delay_global = int(attackDelayUI.get())
            # print("MP here: ", from_mp_global , to_mp_global)
        except TypeError:
            attack_delay_global = 100
            print("Invalid input Attack Delay")

    def re_assign_time_and_key_buff(num):
        for var in range(len(var_list)):
            key_options[var] = var_list[var].get()
            buff_delay[var] = buff_reset_time[var].get()
            buff_state[var] = buff_state_ui[var].get()

    def panic():
        os._exit(0)

    # Some variables to use
    canvas_width = 100
    canvas_height = 10
    OPTIONS = list(key_codes.keys())
    # Some variables to use

    # default panel size
    root.geometry('{}x{}'.format(550, 600))

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
                ).grid(row=row,
                       column=0,
                       sticky=W)

    Label(root,
          text="Attack Delay (ms):"
          ).grid(column=1,
                 row=row)

    Entry(root,
          textvariable=attackDelayUI,
          width=8).grid(column=2,
                        row=row)

    Button(root,
           text='Set',
           command=set_attack_delay
           ).grid(column=5,
                  row=row)

    #Auto Pickup Row
    row += 1
    Checkbutton(root,
                text='Auto Pickup',
                command=change_auto_pickup_state,
                variable=is_auto_pickup,
                ).grid(row=row, column=0, sticky=W)

    #Move Left Row
    row += 1
    Checkbutton(root,
                text='Move Around Map',
                command=change_keep_center,
                variable=is_keep_center,
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
    note_text = Label(root, text="Notes:"
                                 "\nF3 to toggle Auto Attack."
                                 "\nF4 to toggle Auto Pickup."
                                 "\nF8 to toggle Move Around."
                                 "\nAll time variables is in "
                                 "\nmilliseconds (1s = 1000ms).")
    note_text.grid(row=row, sticky=W)

    #Panic button
    row += 1
    Button(root,
           text='Panic Button',
           command=panic,
           height=4,
           width=12,
           ).grid(column=5,
                  row=row)

    root.mainloop()

    return

def on_press_reaction(event):
    #https://stackoverflow.com/questions/47184374/increase-just-by-one-when-a-key-is-pressed/47184663
    global is_auto_attack, is_auto_pickup, is_move_left, is_move_right, is_keep_center
    if event.name == 'f3': # attack
        is_auto_attack = not is_auto_attack
        print("Auto attack state %s" % is_auto_attack)
    if event.name == 'f4': # pick up
        is_auto_pickup = not is_auto_pickup
        print("Auto pick up state %s" % is_auto_pickup)
    if event.name == 'f8':
        is_keep_center = not is_keep_center
        print("Keep center state %s" % is_keep_center)
    # if event.name == 'f5': # move left
    #     if is_move_right == 1:
    #         is_move_right = 0
    #     is_move_left = not is_move_left
    #     print("Move left state %s" % is_move_left)
    # if event.name == 'f6': # move right
    #     if is_move_left == 1:
    #         is_move_left = 0
    #     is_move_right = not is_move_right
    #     print("Move right state %s" % is_move_right)

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
    # time.sleep(1)
    threading.Thread(target=ui).start()
    threading.Thread(target=main(windowName)).start()

    # write_walls()    # <-to uncomment replace first #





