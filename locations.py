"""
Arianna Ford
2022_02_03
Locations
Locations
"""
import player
from MyUtilities import *
from time import *
import sys
import GameBoard 
import hud
import OriginalFruit
import time
import Market

class Location: #basic location class
    def __init__(self, user1):
        self.manager = player.Player()
        self.user1 = user1
        self.foreColor = "white"
        self.backColor = "black"

    def Enter(self, user1):
        color = getattr(term, self.foreColor+"_on_"+self.backColor)
        print(color("Hello!"))
        Town.Enter(self, user1)
        
    def Exit(self, user1):
        color = getattr(term, self.foreColor+"_on_"+self.backColor)
        print(color("Goodbye!"))
        

class Town(Location): #town, main location where you access other places. 
    def __init__(self, user1):
        self.manager = player.Player.genPlayerName()
        self.backColor = "black"
        self.foreColor = "yellow"
        self.palace = Palace(user1 )
        self.lumbermill = Lumbermill(user1)
        self.dungeon = Dungeon(user1)
        self.market = Market.Market(user1)
        self.orchardlocation = OriginalFruit.Orchard(user1)
        self.week = 1
        self.seasonNum = 0
        self.season = ["spring","summer","fall","winter"]
        
    def Enter(self, user1):
        while True:
            ClearScreen()
            print (term.peachpuff("It is week "+str(self.week)+" of "+str(self.season[self.seasonNum]))) #displaying time, manager and directions
            print(term.peachpuff("Hi! Welcome to TownsVille! I am "+self.manager+"!"+"\n"+
            """Where would you like to go?\n
            (P)alace\n
            (L)umbermill\n
            (D)ungeon\n
            (M)arket\n
            (V)iew Player\n
            (Q)uit
            """))

            menuChoice = chr(GetKey()).upper()

            if menuChoice == "P": #entrance to palace
                rest = self.palace
                rest.Enter(user1)
                if rest == "REST":
                    Town.Upkeep(self) #time passing here
                continue

            elif menuChoice == "L": #entrance to lumbermill
                self.lumbermill.Enter()
                continue

            elif menuChoice == "D": #entrance to dungeon
                if self.dungeon.Enter(user1) == "death":
                    ClearScreen()
                    time.sleep(.3)
                    for i in ("You Died..."):
                        print (i, end = "")
                        time.sleep(.5)
                        input()
                        sys.exit(0)

            elif menuChoice == "M": #entrance to market
                self.market.EnterMarketArea()

            elif menuChoice == "V": #option to view player
                ClearScreen()
                print (term.yellow(user1.name))
                print (term.yellow(user1.history))
                print (term.red("Attack: " + str(user1.attack)))
                print (term.green("Defense: " + str(user1.defense)))
                input()

            elif menuChoice == "Q": #option to quit game
                self.Exit()

            else: #continuing so no errors occur
                pass


    def Exit(): #basic exit option
        sys.exit(0)

    def Upkeep(self): #time passing
        self.week +=1
        if self.lumbermill.stock >= self.lumbermill.capacity:
            print("The stock of the Lumbermill is now full. ")
        else:
            self.lumbermill.stock += self.lumbermill.rate
        if self.week >13:
            self.week = 1
            if self.seasonNum >= 3:
                self.seasonNum = 0
                self.season = 0
            else:
                self.season +=1


class Palace(Location):
    def __init__(self, user1, foreColor = "goldenRod"):        
        self.manager = user1
        self.backColor = "black"
        self.foreColor = foreColor
        self.playerGoldNum = user1.gold
        self.palaceGoldNum = 10
        
        
    def Enter(self, user1):
        self.user1 = user1
        while True:
            ClearScreen() #directons on what to do in the palace 
            palaceChoice = input(term.yellow("""What would you like to do in the Palace?\n 
            (D)eposit gold\n
            (R)est\n
            Go to (T)own\n
            Gold currently in Palace: """+str(self.palaceGoldNum))).upper()
            if palaceChoice == "D":
                while True:
                    ClearScreen()
                    transferAmount = input(term.yellow("How much would you like to tansfer? You have "+str(self.playerGoldNum)+" gold.(0) to exit. "))
                    if transferAmount.isdigit(): #making sure player entered number
                        self.palaceGoldNum += int(transferAmount) 
                        self.playerGoldNum -= int(transferAmount)
                    
                    if int(transferAmount) > self.playerGoldNum: #making sure player has enough to transfer
                        ClearScreen()
                        print(term.yellow("You do not have enough to tansfer "+str(transferAmount)+". "))
                        continue
                    elif int(transferAmount) <= self.playerGoldNum: #allowing transaction to occur
                        ClearScreen()
                        print(term.yellow("You deposited "+str(transferAmount)+" into the palace. "))
                        break
                    elif int(transferAmount) == 0:
                        break
                    else:
                        print(term.brown("Please enter a valid input. "))
                        input()
                        continue
                        
            elif palaceChoice == "R": #time passing by sleeping
                ClearScreen()
                print ("Have a good sleep!")
                input()
                ClearScreen()
                return "REST"
            elif palaceChoice == "T": #going back to town
                break
            else:
                print("Please enter a valid input. ")
                input()
                continue
        
    def Exit(self, user1):
        ClearScreen()
    

class Lumbermill(Location):
    def __init__(self, user1):
        self.user1 = user1
        self.manager = player.Player(0, 0, "O", "yellow", 0, 0, 0)
        self.foreColor = "goldenrod"
        self.backColor = "black"
        self.rate = 100
        self.capacity = 10000
        self.stock = 0

    def Enter(self): #entering the lumbermill and providing information
        ClearScreen()
        color = getattr(term, self.foreColor+"_on_"+self.backColor)
        print(color("""Hello, welcome to the Lumbermil!\n
        The rate at which lumber is gathered is """+str(self.rate)+""" per week. \n
        The max capacity we can hold here is """+str(self.capacity)+"""\n
        The current amount of wood being held is """+str(self.stock)+". "))
        input()


class Dungeon(Location):
    def __init__(self, user1):
        self.user1 = user1
        self.defeatAll = False

    def Enter(self, user1): #entering dungeon
        ClearScreen()
        dungeonHud = hud.Hud()
        dungeonHud.PlayerWindow(user1)
        dungeonHud.EnemyWindow()
        dungeonHud.ItemWindow()
        dungeonHud.SystemHud()
        board = GameBoard.Board()
        board.CreateBoard("Dungeon", "#")
        board.CreateRooms(10, "dungeon")
        board.BuildCorridors()
        board.PlaceStairs() 
        board.PlacePotion()
        user1.PlaceActor(board, "yellow", "player", "dungeon")
        board.ShowBoard()
        monsterNum = {0:"monster0", 1:"monster1", 2:"monster2", 3:"monster3", 4:"monster4", 5:"monster5", 6:"monster6"}
        #, 7:"monster7", 8:"monster8", 9:"monster9"
                  
        for spot in range(len(monsterNum)): #placing all enemies
            monsterNum[spot] = player.Demon(0, 0, "¤", "black", 0, 0, 0)
            monsterNum[spot].PlaceActor(board, "black", "monster", "dungeon") 
            board.boardSize[monsterNum[spot].row][monsterNum[spot].col].DisplayTile() 
        if user1.floorLevel == 100: #testing if game has been beat
            ClearScreen()
            print (""" __   __           __        __          _ 
 \ \ / /__  _   _  \ \      / /__  _ __ | |
  \ V / _ \| | | |  \ \ /\ / / _ \| '_ \| |
   | | (_) | |_| |   \ V  V / (_) | | | |_|
   |_|\___/ \__,_|    \_/\_/ \___/|_| |_(_)""")
            input()
            sys.exit(0)

        else:
            while True: 
                user1.InventoryCheck()#displaying user inventory
                user1.ItemUse()
                MoveCursor(17,62)#updates
                print ("steps: "+str(user1.steps)) #updates
                MoveCursor(18,62)#updates
                print ("Floor level:"+str(user1.floorLevel))#updates
                MoveCursor(12,62)#updates
                print (term.yellow("Gold: " + str(user1.gold)))#updates
                if len(monsterNum) >= 1: #testing to see if monster list is long enough
                    for x in range(len(monsterNum)):#if it is, cycling through and jumping over empty spaces to prevent errors caused by holes in list
                        while True:
                            if x not in monsterNum:
                                x +=1
                                if x not in monsterNum:
                                    x = 0
                                    continue
                                continue
                            else:
                                break
                        healthDecrease = user1.attack - monsterNum[x].defense 
                        if monsterNum[x].health - healthDecrease >1: #testing damage against enemy
                            areaTest =  monsterNum[x].AreaTest(user1, dungeonHud, monsterNum, x)
                            monsterNum[x].MonsterMove(board, monsterNum, x, dungeonHud, user1, areaTest)
                        else: #testing if enemy is dead
                            monsterNum[x].Death(dungeonHud, board, monsterNum, x, user1)
                            continue
                    else:  #allowing player to move
                        userMove = chr(GetKey()).upper()
                        while True:
                            if x not in monsterNum:
                                x +=1
                                if x not in monsterNum:
                                    x = 0
                                    continue
                                continue
                            else:
                                break
                        healthDecrease = monsterNum[x].attack - user1.defense #allowing player to take damage from enemy
                        if user1.health - healthDecrease >1:
                            userPlayGame = user1.MoveActor(board,dungeonHud, "yellow", user1, userMove, "player", monsterNum[x])
                        else:
                            return "death"
                else: #if all enemies have been beat
                    dungeonHud._message.append("You defeated all the monsters! ")
                    dungeonHud.colorsList.append("yellow")
                    dungeonHud.SystemMessage() 
                    self.defeatAll = True
                    userMove = chr(GetKey()).upper()
                    userPlayGame = user1.MoveActor(board,dungeonHud, "yellow", user1, userMove, "player", monsterNum)
                userPlayGame

                if userPlayGame == "exit": #return from player move
                    break
                elif userPlayGame == "continue": #return from player move
                    continue

                elif userPlayGame == "wallMessage": #return from player move
                    dungeonHud._message.append("Thats a wall you're running into...")
                    dungeonHud.colorsList.append("orange")
                    dungeonHud.SystemMessage()

                elif userPlayGame == "potionMessage": #return from player move
                    #allows player to recieve potion
                    potionNum = random.randint(1,3)
                    if potionNum == 1:
                        potionType = "health"
                    elif potionNum == 2:
                        potionType = "strength"
                    elif potionNum == 3:
                        potionType = "unknown"
                    potion = ("potion of "+str(potionType))
                    user1.inventory.append(potion)

                elif userPlayGame == "stairsMessage": #return from player move
                    #goes to another floor in the dungeon
                    user1.InventoryCheck()
                    user1.ItemUse()
                    user1.floorLevel += 1
                    dungeonHud._message.append("Going to next level... ")
                    dungeonHud.colorsList.append("orange")
                    dungeonHud.SystemMessage()
                    time.sleep(1)
                    ClearScreen()
                    dungeonHud = hud.Hud()
                    dungeonHud.PlayerWindow(user1)
                    dungeonHud.EnemyWindow()
                    dungeonHud.ItemWindow()
                    dungeonHud.SystemHud()
                    board = GameBoard.Board()
                    board.CreateBoard("Dungeon", "#")
                    board.CreateRooms(10, "dungeon")
                    board.BuildCorridors()
                    board.PlaceStairs() 
                    board.PlacePotion()
                    user1.PlaceActor(board, "yellow", "player", "dungeon")
                    board.ShowBoard()
                    monsterNum = {0:"monster0", 1:"monster1", 2:"monster2", 3:"monster3", 4:"monster4", 5:"monster5", 6:"monster6", 7:"monster7", 8:"monster8"}
                    #, 9:"monster9"
                    for spot in range(len(monsterNum)):
                        monsterNum[spot] = player.Demon(0, 0, "¤", "black", 0, 0, 0)
                        monsterNum[spot].PlaceActor(board, "black", "monster", "dungeon") 