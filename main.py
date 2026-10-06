"""
Arianna Ford
2022_01_31
main.py
"""
import sys
from player import *
from color_extractor import *
import locations
from MyUtilities import *
import subprocess

def Main():
    #HideCursor() throws this error: Could not find module 'kernel123' (or one of its dependencies). Try using the full path with constructor syntax.
    #os.system('mode con: cols=100 lines=60')#sets default size of screen for player. 
    cmd = ["mode", "con", "cols=100", "lines=60"]#sets default size of screen for player. 
    result = subprocess.run(cmd, shell=True, check=True)

    #Previous 3 lines of code were added 10/5/2026 as a result of os.system being depreciated

    ClearScreen()
    while True: #display title screen with option to play
        print (term.red("""\n █    ██  ███▄    █ ▓█████▄ ▓█████  ██▀███         █     █░ ▒█████   ██▀███   ██▓    ▓█████▄ 
 ██  ▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒      ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒▓██▒    ▒██▀ ██▌
▓██  ▒██░▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒      ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒▒██░    ░██   █▌
▓▓█  ░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄        ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ▒██░    ░▓█▄   ▌
▒▒█████▓ ▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒      ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒░██████▒░▒████▓ 
░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░      ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒░▓  ░ ▒▒▓  ▒ 
░░▒░ ░ ░ ░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░        ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░░ ░ ▒  ░ ░ ▒  ▒ 
 ░░░ ░ ░    ░   ░ ░  ░ ░  ░    ░     ░░   ░         ░   ░  ░ ░ ░ ▒    ░░   ░   ░ ░    ░ ░  ░ 
   ░              ░    ░       ░  ░   ░               ░        ░ ░     ░         ░  ░   ░    
                     ░                                                                ░      """))


        MoveCursor(55, 0)
        print (term.yellow("Are you able to reach level 100?"))
        MoveCursor(56, 0)
        print(term.yellow("""╔═╗  ┌┬┐┌─┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐
╚═╗   │ │ │  └─┐ │ ├─┤├┬┘ │ 
╚═╝   ┴ └─┘  └─┘ ┴ ┴ ┴┴└─ ┴ """))
        print ("Created by Arianna Ford. ")
        userInput = chr(GetKey()).upper()
        if userInput == "S":
            while True:
                while True: #let player choose if they like player or not
                    user1 = Player(0, 0, "O", "yellow", 0, 0, 0)
                    ClearScreen()
                    print (term.yellow(user1.name))
                    print (term.yellow(user1.history))
                    print (term.red("Attack: " + str(user1.attack)))
                    print (term.green("Defense: " + str(user1.defense)))
                    print(term.yellow("Are you okay with this player? (Y/N)"))
                    choosePlayer = chr(GetKey()).upper()
                    if choosePlayer == "N":
                        continue
                    elif choosePlayer == "Y":
                        break
                    else:
                        print ("Please enter a valid input. ")
                        continue
                town = locations.Town(user1) #entering game
                town.Enter(user1)
                input()
        elif userInput == "N": #exiting game
            sys.exit(0)
        else:
            print ("Please enter a valid input. ") #error prevention
            continue
Main()
