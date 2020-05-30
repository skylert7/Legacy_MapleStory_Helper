from multiprocessing import Process
from random import randint

from pywinauto.keyboard import send_keys
import threading
import time
from read_pos import read_pos

runs = 0
lock = threading.Lock()


def walk(direction, ):
    if direction == 'right' :
        send_keys('{RIGHT down}'
                  )
        time.sleep(0.15)
        send_keys('{RIGHT up}'
                  )
    else:
        send_keys('{LEFT down}'
                  )
        time.sleep(0.15)
        send_keys('{LEFT up}'
                  )


def walk_delay(direction, delay):
    if direction == 'right' :
        send_keys('{RIGHT down}'
                  )
        time.sleep(delay)
        send_keys('{RIGHT up}'
                  )
    else:
        send_keys('{LEFT down}'
                  )
        time.sleep(delay)
        send_keys('{LEFT up}'
                  )


def up_down_delay(direction, delay):
    if direction == 'up' :
        send_keys('{UP down}'
                  )
        time.sleep(delay)
        send_keys('{UP up}'
                  )
    else:
        send_keys('{down down}'
                  )
        time.sleep(delay)
        send_keys('{down up}'
                  )


def jump(delay):
    send_keys('{VK_MENU}')
    time.sleep(delay)
    send_keys('{VK_MENU}')


def func1():
    global runs
    lock.acquire()
    lock.release()
    while runs < 20:
        send_keys('{c down}'
                  '{c up}'
                  )
        runs += 1


def func2():
    global runs
    lock.acquire()
    lock.release()
    while runs < 20:
        send_keys('{s down}'
                  '{s up}'
                  )
        runs += 1


def func3():
    global runs
    global lock
    lock.acquire()
    lock.release()
    while runs < 20:
        send_keys('{RIGHT down}'
                  '{RIGHT up}'
                  )
        runs += 1


def func4():
    global runs
    global lock
    lock.acquire()
    lock.release()
    while runs < 20:
        send_keys('{LEFT down}'
                  '{LEFT up}'
                  )
        runs += 1


def start_right():
    p3 = Process(target=func3)
    p3.start()
    time.sleep(0.011)
    p1 = Process(target = func1)
    p1.start()
    time.sleep(0.004)
    p2 = Process(target = func2)
    p2.start()


def start_left():
    p3 = Process(target=func4)
    p3.start()
    time.sleep(0.011)
    p1 = Process(target = func1)
    p1.start()
    time.sleep(0.004)
    p2 = Process(target = func2)
    p2.start()


def write_walls():
    f = open('file.txt', 'a+')
    userInput = input("press enter: ")

    while userInput != 'q':
        x, y = read_pos()

        f.write(str(x) + ' ' + str(y) + '\n')
        print(x, y)
        userInput = input("press enter to read again")

    f.close()


def platform_attack():
    right_wall = 1068 ## Run
    left_wall = -838

    zerod = abs(left_wall)

    left_wall = left_wall + zerod ## I prefer the values to be zero'd
    right_wall = right_wall + zerod 

    ##             |            |           |           |           |              ##
    ##     LW            L82         L81    M    R81         R82           RW      ##

    middle = (right_wall - left_wall) / 2
    right_quad = middle + middle / 2
    left_eight_1 = middle - middle / 4

    x, y = read_pos()
    x += zerod 
    y += zerod 

    if  x >= right_quad:
        walk('left')
        start_left()
        time.sleep(3)
    elif x <= left_eight_1:
        walk('right')
        start_right()
        time.sleep(3)

    else:
        rand = randint(1, 11)
        if rand//2 == 0:
            walk('right')
            start_right()
            time.sleep(3)
        else:
            walk('left')
            start_left()
            time.sleep(3)


''' Used for HSing people,  walking to spot'''

def move_to_x_target(target_x):
    x, y = read_pos()

    while abs(x-target_x) > 50:

        if x - target_x  > 0:
            walk_delay('left', 0.5)
        elif x - target_x  < 0:
            walk_delay('right', 0.5)
        x, y = read_pos()

''' Working on a platform  helper function'''

# def move_to_y_target(target_y):
#     x, y = read_pos()
#
#     while abs(y-target_y) > 1:
#         jump(0.1)
#         up_down_delay('up', 0.1)
#         x, y = read_pos()


''' Working on a platform switcher for Skeles map'''

# def switch_platforms(x_target, y_target):
#     x, y = read_pos()
#     while (abs(y - y_target) > 1):
#         if (abs(x-x_target) > 10):
#             move_to_x_target(x_target)
#         else:
#             move_to_y_target(y_target)
