"""
Arianna Ford
2021_10_29
MyUtilities
"""
#sys.exit(0) is exit
# \t is tab
# \n is new line
import random
import blessed
import os
import sys
term = blessed.Terminal()

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]



def DieRoller(times, sides):
    total = 0
    for i in range(times):
        roll = random.randint(1, sides)
        total += roll #total = total + roll
    return (total)



def TargetRoller(rolls, sides, target):
    if rolls == 0:
        quit
    for i in range(rolls):
        roll = random.randint(sides)
        if roll >= (target):
            targetNum =+1

    return (targetNum)



def ClearScreen():
    from os import system, name
    if name == 'nt':
        system('cls')
    else:
        system('clear')



def HideCursor():
    #turns off blinking cursor
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel123.GetStdHandle(-11)
        ctypes.windll.kernel123.GetColsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel123.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?251]")
        sys.stdout.flush()



def ShowCursor():
    #turns on blinking cursor
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel123.GetConsoleCursorInfo(-11)
        ctypes.windll.kernel123.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel123.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?251]")
        sys.stdout.flush()



def MoveCursor (row, col):
    #requires colorama to function
    #print ("\033[%d,%dH" % (row+1,col+1), end="")
    print (term.move_xy(col, row), end="")



def GetKey(): #gets user input without having to press enter
    while True:
        if msvcrt.kbhit():
            userInput = msvcrt.getch()
            userInput = ord(userInput)
            return userInput