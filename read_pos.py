from ReadWriteMemory import *


def read_pos():

    rwm = ReadWriteMemory()

    process = rwm.get_process_by_name('MapleHome.dll')
    process.open()

    x_pointer = process.get_pointer(0x00BEBF98, offsets=[0x116C])
    y_pointer = process.get_pointer(0x00BEBF98, offsets=[0x1170])

    x = process.read(x_pointer)
    y = process.read(y_pointer)

    if x > 99999:
        x = x - 4294967294
    if y > 99999:
        y = y - 4294967294
    process.close()

    return x, y

