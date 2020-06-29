# Version 1.4
# Released Date: 6/29/2020

from import_standalone import *
from screen_processing import *
from playsound import playsound

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
is_keep_center = 0
is_move_around = 0

from_mp_global = 50 # percent
to_mp_global = 60 # percent
from_hp_global = 70 # percent
to_hp_global = 80 # percent
attack_delay_global = 100 # milliseconds
buff_delay = [200, 200, 600, 0]
buff_state = [0] * len(buff_delay)
moveDelay = [1000, 1000]  # [left, right] in milliseconds

key_options = ["String"] * len(buff_delay)

user_coor_global = (0, 0) # user coordinate
user_coor_center_point = (0, 0) # user coordinate center point to run around
keep_center_calibration_global = 0 # bias to left or right
keep_center_left_wall_is_reached = False # var for keep_center
keep_center_right_wall_is_reached = False # var for keep_center
left_area_is_reached = False # var for move_around
right_area_is_reached = False # var for move_around
keep_center_radius = 40 # var for keep_center
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

    # im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("Window image", im_np)
    # cv2.waitKey()
    return im_np

def check_for_chaos_scroll():
    global windowName
    img_rgb = get_window_image(windowName)
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Read the template
    template1 = cv2.imread('CS_1024x768.JPG', 0)
    template2 = cv2.imread('CS_1280x920.JPG', 0)

    # Store width and height of template in w and h
    w1, h1 = template1.shape[::-1]
    w2, h2 = template1.shape[::-1]

    # Perform match operations.
    res1 = cv2.matchTemplate(img_gray, template1, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.8

    # Store the coordinates of matched area in a numpy array
    loc1 = np.where(res1 >= threshold)
    loc2 = np.where(res2 >= threshold)
    if len(loc1[0]) > 0:
        return True

    if len(loc2[0]) > 0:
        return True
    # Draw a rectangle around the matched region.
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    #     # Show the final image with the matched area.
    # cv2.imshow('Detected', img_rgb)
    # cv2.waitKey()
    return False

def get_user_coord():
    global user_coor_global
    user_coor = (0, 0)
    w_minmap = 0
    try:
        # Screen Processing
        dx = MapleScreenCapturer()
        hwnd = dx.ms_get_screen_hwnd()
        rect = dx.ms_get_screen_rect(hwnd)

        static = StaticImageProcessor(dx)
        static.update_image()
        # Screen Processing

        x_minmap, y_minmap, w_minmap, h_minmap = static.get_minimap_rect()
        user_coor = static.find_player_minimap_marker(rect=[x_minmap, y_minmap, w_minmap, h_minmap])  # tuple

        user_coor_global = user_coor
        # print(user_coor)
        # print("User global coor", user_coor_global)
    except Exception as e:
        # print(e)
        pass
    return user_coor, w_minmap

def display_state_info():
    os.system('cls')
    global is_auto_hp, \
        is_auto_mp, \
        is_auto_attack, \
        is_keep_center, \
        is_move_around, \
        is_auto_pickup

    print('Auto HP State: {}\n'
          'Auto MP State: {}\n'
          'Auto Attack State: {}\n'
          'Auto Pickup State: {}\n'
          'Keep Center State: {}\n'
          'Move Around State: {}\n'.format(is_auto_hp,
                                           is_auto_mp,
                                           is_auto_attack,
                                           is_auto_pickup,
                                           is_keep_center,
                                           is_move_around)
          )
    print('--- Press F12 to terminate ---')
    return

def keep_center():
    global keep_center_calibration_global, \
        keep_center_radius, \
        keep_center_left_wall_is_reached, \
        keep_center_right_wall_is_reached, \
        user_coor_center_point
    if not keep_center_left_wall_is_reached and not keep_center_right_wall_is_reached:
        keep_center_left_wall_is_reached = True

    try:
        user_coor, w_minmap = get_user_coord()

        if user_coor[0] == 0:
            return

        # wall = []
        wall = [user_coor_center_point[0] - keep_center_radius,
                user_coor_center_point[0] + keep_center_radius]
        # print(wall)

        if user_coor[0] < wall[0]: # wall left
            keep_center_left_wall_is_reached = True
            keep_center_right_wall_is_reached = False

        if user_coor[0] > wall[1]: # wall right
            keep_center_right_wall_is_reached = True
            keep_center_left_wall_is_reached = False
            # print("In Right")

        if not keep_center_left_wall_is_reached:
            move_left_mage()
            # print("Move Left")

        else:
            move_right_mage()
            # print("Move Right")


    except Exception as e:
        print(e)
        # print(user_coor)
        move_right_mage()
        move_left_mage()
        # move_up_mage()

def move_around():
    global left_area_is_reached, right_area_is_reached
    if not left_area_is_reached and not right_area_is_reached:
        left_area_is_reached = True

    try:
        user_coor, w = get_user_coord()

        far_right = int(85*w/100)
        far_left = int(20*w/100)

        if user_coor[0] < far_left:
            left_area_is_reached = True
            right_area_is_reached = False
            # print("In Left")

        if user_coor[0] > far_right:
            right_area_is_reached = True
            left_area_is_reached = False
            # print("In Right")

        if not left_area_is_reached:
            move_left_mage()
        else:
            move_right_mage()
    except:
        move_right_mage()
        move_left_mage()

    return

def lie_detector():
    return False

def main():
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
        is_keep_center, \
        is_move_around

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
    time_at_check = datetime.utcnow()
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

        # It does what it says
        if is_keep_center == 1:
            keep_center()

        # Move Around Map Horizontally
        if is_move_around == 1:
            move_around()

        if (datetime.utcnow() - time_at_check).total_seconds() > 60:
            if check_for_chaos_scroll():
                playsound("Windows_Unlock.wav")
                time_at_check = datetime.utcnow()

def ui():
    global maple_story
    # Global for True/False var
    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup,\
        is_keep_center, \
        is_move_around, \
        resOption, \
        buff_state
    # Global for string/int var
    global to_mp_global, \
        to_hp_global, \
        from_mp_global, \
        from_hp_global, \
        attack_delay_global, \
        keep_center_radius, \
        user_coor_global, \
        user_coor_center_point, \
        buff_delay, \
        key_options

    root = Tk()

    # UI Vars

    is_auto_hp = IntVar(value=int(is_auto_hp))
    is_auto_mp = IntVar(value=int(is_auto_mp))
    is_auto_attack = IntVar(value=int(is_auto_attack))
    is_auto_pickup = IntVar(value=int(is_auto_pickup))
    is_keep_center = IntVar(value=int(is_keep_center))
    is_move_around = IntVar(value=int(is_move_around))

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

    keepCenterRadiusUI = StringVar()
    keepCenterRadiusUI.set(str(keep_center_radius))

    userCoordinateUI = StringVar()
    userCoordinateUI.set('({}, {})'.format(user_coor_global[0], user_coor_global[1]))

    buff_reset_time = list()
    buff_state_ui = list()
    # UI Vars ---

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

    root.title("MapleStory Helper")


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

    def change_move_around():
        global is_move_around
        is_move_around = not is_move_around
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

    def set_keep_center_radius():
        global keep_center_radius
        try:
            keep_center_radius = int(keepCenterRadiusUI.get())
        except:
            keep_center_radius = 15
            print("Invalid input radius")

    def get_user_coordinate_center_point_ui():
        global user_coor_center_point
        try:
            user_coor_center_point, w_random = get_user_coord()
        except:
            user_coor_center_point = (0, 0)
        userCoorLabel['text'] = '({}, {})'.format(user_coor_center_point[0], user_coor_center_point[1])

    def re_assign_time_and_key_buff(num):
        for var in range(len(var_list)):
            key_options[var] = var_list[var].get()
            buff_delay[var] = buff_reset_time[var].get()
            buff_state[var] = buff_state_ui[var].get()

    def update_status():
        return

    def panic():
        os._exit(0)

    # Some variables to use
    canvas_width = 100
    canvas_height = 10
    OPTIONS = list(key_codes.keys())
    # Some variables to use

    # default panel size
    root.geometry('{}x{}'.format(550, 650))

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
    #Auto Attack Row ---

    #Auto Pickup Row
    row += 1
    Checkbutton(root,
                text='Auto Pickup',
                command=change_auto_pickup_state,
                variable=is_auto_pickup,
                ).grid(row=row,
                       column=0,
                       sticky=W)
    #Auto Pickup Row ---

    #Keep Center Row
    row += 1
    Checkbutton(root,
                text='Keep Center',
                command=change_keep_center,
                variable=is_keep_center,
                ).grid(row=row,
                       column=0,
                       sticky=W)

    Button(root,
           text="Get User \nPosition",
           command=get_user_coordinate_center_point_ui
           ).grid(column=1,
                  row=row)
    userCoorLabel = Label(root,
                          text=userCoordinateUI
                          )

    userCoorLabel.grid(column=2,
                       row=row)

    Label(root,
          text="Radius:"
          ).grid(column=3,
                 row=row)

    Entry(root,
          textvariable=keepCenterRadiusUI,
          width=8).grid(column=4,
                        row=row)

    Button(root,
           text='Set',
           command=set_keep_center_radius
           ).grid(column=5,
                  row=row)

    #Keep Center Row ---

    #Move Around Row
    row += 1
    Checkbutton(root,
                text='Move Around',
                command=change_move_around,
                variable=is_move_around,
                ).grid(row=row,
                       column=0,
                       sticky=W)

    #Move Around Row ---

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
              text="Reset Time (s):").grid(column=1,
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
    note_text = Label(root,
                      text="Notes:"
                           "\nF3 to toggle Auto Attack."
                           "\nF4 to toggle Auto Pickup."
                           "\nF8 to toggle Keep Center."
                           "\nF9 to toggle Move Around."
                           "\nF12 to terminate all."
                      )
                                 # "\nAll time variables is in "
                                 # "\nmilliseconds (1s = 1000ms).")
    note_text.grid(row=row, sticky=W)

    #Panic button
    row += 1
    Button(root,
           text='Panic Button (F12)',
           command=panic,
           height=4,
           width=16,
           ).grid(column=5,
                  row=row)


    root.mainloop()

    return

def on_press_reaction(event):
    #https://stackoverflow.com/questions/47184374/increase-just-by-one-when-a-key-is-pressed/47184663
    global is_auto_attack, \
        is_auto_pickup, \
        is_move_left, \
        is_move_right, \
        is_keep_center, is_move_around

    if event.name == 'f1': # info
        display_state_info()
    if event.name == 'f3': # attack
        is_auto_attack = not is_auto_attack
        print("Auto attack state %s" % is_auto_attack)
    if event.name == 'f4': # pick up
        is_auto_pickup = not is_auto_pickup
        print("Auto pick up state %s" % is_auto_pickup)
    if event.name == 'f8':
        if is_move_around == 1:
            is_move_around = 0
        is_keep_center = not is_keep_center
        print("Keep center state %s" % is_keep_center)
    if event.name == 'f9':
        if is_keep_center == 1:
            is_keep_center = 0
        is_move_around = not is_move_around
        print("Move around state %s" % is_move_around)
    if event.name == 'f12':
        os._exit(0)
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
    time.sleep(1)
    threading.Thread(target=ui).start()
    threading.Thread(target=main()).start()

    # while True:
    #     exchange_giftbox()
    #     time.sleep(randint(1, 4))



    # write_walls()    # <-to uncomment replace first #





