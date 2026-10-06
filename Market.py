"""
Arianna Ford
2022_04_27
Market
"""
from GameBoard import *
from hud import * 
from MyUtilities import *
import time

class Market:
    def __init__(self, user1):
        self.user1 = user1

    def Buy(self, list, desc, userShop): #when item is bought
        desc.pop(userShop-1)
        self.user1.inventory.append(list.pop(userShop-1))
        

    def Shop(self, list, desc): #when window shopping
        while True:
            MoveCursor(31, 62)
            print (" "*35)
            MoveCursor(32, 62)
            print (" "*35)
            MoveCursor(32, 62) #clearing section
            print ("(E)xit Shop")
            for i in range(6):
                row = 22
                MoveCursor(row+i, 62)
                print (" "*45)  #clearing section
            for i in range(len(list)):
                row = 22
                MoveCursor(row+i, 62)
                print ("("+str(i)+")"+list[i]) #displaying shop items
            while True:
                userShop = chr(GetKey()).upper() 
                if userShop == "E":
                    break
                try: 
                    userShop = int(userShop) #testing to make sure user input is a number to prevent errors
                    if userShop <= (len(desc)):
                        break
                except ValueError:
                    continue
                
            for i in range(12):
                row = 22
                MoveCursor(row+i, 62)
                print (" "*45) #clearing screen
            if userShop == "E":
                break
            else:
                MoveCursor(22, 62)
                print (desc[(int(userShop))]) #displaying description of item
                MoveCursor(30, 62)
                print ("You have "+str(self.user1.gold)+" gold.") #reminding player how much gold they have
                MoveCursor(31, 62)
                price = len(list[userShop])
                print ("(B)uy Item? Price is "+str(price)+" gold.") #displaying price
                MoveCursor(32, 62)
                print ("(N)evermind!") #option to back out
                choice = chr(GetKey()).upper()
                if choice == "B": #buying item
                    if self.user1.gold >= price:
                        self.Buy(list, desc, userShop)
                        self.user1.gold -= price
                        MyUtilities.MoveCursor(12,62)
                        print (" "*35)  
                        MyUtilities.MoveCursor(12,62)
                        print (term.yellow("Gold: "+str(self.user1.gold)), flush=True) #redisplaying gold amount that player has
                        MoveCursor(30, 62)
                        print ("You have "+str(self.user1.gold)+" gold.")            
                    else:
                        MoveCursor(31, 62)
                        print (" "*35)
                        MoveCursor(32, 62)
                        print (" "*35)
                        MoveCursor(31, 62) #clearing screen
                        print ("You don't have enough gold... ")
                        MoveCursor(32, 62)
                        print ("Try killing more enemies. ")
                        time.sleep(2.5)
                elif choice == "N":
                    continue
                continue


    def EnterMarketArea(self):
        ClearScreen() 
        self.user1.InventoryCheck()
        self.user1.ItemUse()
        MyUtilities.MoveCursor(12,62)
        print (term.yellow("Gold: "+str(self.user1.gold)), flush=True)
        marketHud = Hud()
        marketHud.MarketWindows(self.user1)
        yard  = Board()
        yard.CreateBoard("yard", ",")
        yard.CreateRooms(5, "yard")
        self.createWall(yard)
        self.createPath(yard)
        self.user1.PlaceActor(yard, "yellow", "player", "market")
        yard.ShowBoard()
        self.createSign("apothecary")
        self.createSign("grocery")
        self.createSign("weaponry")
        self.createSign("armory")
        MoveCursor(1,62)
        print ("W/A/S/D to move in the Market.")
        MoveCursor(2,62)
        print ("Go back to the entrance to exit!")
        
        while True:
            userMove = chr(GetKey()).upper()
            self.user1.MoveActor(yard,marketHud, "yellow", self.user1, userMove, "player", "market")
            row = self.user1.row
            col = self.user1.col
            #Entrance/exit to Market below
            if row == 49 and col == 26:
                break 
            elif row == 49 and col == 25:
                break
            elif row == 49 and col == 27:
                break

            elif row == 17 and col == 10: #displaying shop items
                apothecaryList = ["potion of strength", "potion of health", "potion of unknown"]
                apothecaryDesc = ["Increases strength by 6. ", "increases health by 10", "?"]
                self.Shop(apothecaryList, apothecaryDesc)
                

            elif row == 10 and col == 39: #displaying shop items
                groceryList = ["apple", "pheonix blossom"]
                groceryDesc = ["Improves health by 5. ", "Improves attack by 10 for 15 steps. "]
                self.Shop(groceryList, groceryDesc)

            elif row == 40 and col == 20: #displaying shop items
                weaponryList = ["sword", "obsidian sword"]
                weaponryDesc = ["Improves attack by 5. ", "Improves attack by 9."]
                self.Shop(weaponryList, weaponryDesc)

            elif row == 36 and col == 47: #displaying shop items
                armoryList = ["helmet", "chestplate", "shield"]
                armoryDesc = ["Improves your defense by 3. ", "Improves your defense by 7. ", "Improves your defense by 5. "]
                self.Shop(armoryList, armoryDesc)

            else:
                for i in range(6): #erasing items from shop after exiting
                    row = 22
                    MoveCursor(row+i, 62)
                    print (" "*25) 



    def createWall(self, yard): #making border so player cannot walk off board
        foreColor = "darkorange4"
        backColor = "orange4"
        for i in range(yard.colLen-1):
            yard.boardSize[0][i].symbol = "#" 
            yard.boardSize[0][i].passable = False
            yard.boardSize[0][i].foreColor = foreColor
            yard.boardSize[0][i].backColor = backColor
        for j in range(yard.rowLen-1):
            yard.boardSize[j][i].symbol = "#" 
            yard.boardSize[j][i].passable = False
            yard.boardSize[j][i].foreColor = foreColor
            yard.boardSize[j][i].backColor = backColor
        for i in range(yard.rowLen-1):
            yard.boardSize[i][0].symbol = "#" 
            yard.boardSize[i][0].passable = False
            yard.boardSize[i][0].foreColor = foreColor
            yard.boardSize[i][0].backColor = backColor
        for j in range(yard.colLen-1):
            yard.boardSize[i][j].symbol = "#" 
            yard.boardSize[i][j].passable = False
            yard.boardSize[i][j].foreColor = foreColor
            yard.boardSize[i][j].backColor = backColor



    def createPath(self, yard): #creating entrance to stores at Market, had plans to make path
        foreColor = "darkorange4"
        backColor = "darkolivegreen"
        colList = [26, 10, 39, 20, 47, 6]
        rowList = [49, 17, 10, 40, 36, 26]
        #Entrance to Market area
        col = colList[0]
        row = rowList[0]
        for i in range(3):
            yard.boardSize[row][col+i].symbol = "+" 
            yard.boardSize[row][col].occupied  = None
            yard.boardSize[row][col+i].passable = True
            yard.boardSize[row][col+i].doorHere = True
            yard.boardSize[row][col+i].foreColor = "darkorange4"
            yard.boardSize[row][col+i].backColor = "darkolivegreen"

        #apothecary entrance
        col = colList[1]
        row = rowList[1]
        yard.boardSize[row][col].symbol = "+" 
        yard.boardSize[row][col].occupied  = None
        yard.boardSize[row][col].passable = True
        yard.boardSize[row][col].doorHere = True
        yard.boardSize[row][col].foreColor = foreColor
        yard.boardSize[row][col].backColor = backColor

        #grocery entrance
        col = colList[2]
        row = rowList[2]
        yard.boardSize[row][col].symbol = "+" 
        yard.boardSize[row][col].occupied  = None
        yard.boardSize[row][col].passable = True
        yard.boardSize[row][col].doorHere = True
        yard.boardSize[row][col].foreColor = foreColor
        yard.boardSize[row][col].backColor = backColor

        #weaponry entrance
        col = colList[3]
        row = rowList[3]
        yard.boardSize[row][col].symbol = "+" 
        yard.boardSize[row][col].occupied  = None
        yard.boardSize[row][col].passable = True
        yard.boardSize[row][col].doorHere = True
        yard.boardSize[row][col].foreColor = foreColor
        yard.boardSize[row][col].backColor = backColor

        #armory entrance
        col = colList[4]
        row = rowList[4]
        yard.boardSize[row][col].symbol = "+" 
        yard.boardSize[row][col].occupied  = None
        yard.boardSize[row][col].passable = True
        yard.boardSize[row][col].doorHere = True
        yard.boardSize[row][col].foreColor = foreColor
        yard.boardSize[row][col].backColor = backColor

    def createSign(self, signType): #makes signs on each building
        foreColor = "black"
        backColor = "orange4"
        getattr(term, (foreColor+"_on_"+backColor))
        fc = foreColor
        bc = backColor
        color = getattr(term, fc+"_on_"+bc)
        #apothecary sign:
        if signType == "apothecary":
            for i in range(len("APOTHECARY")):
                word = {0:"A", 1:"P", 2:"O", 3:"T", 4:"H", 5:"E", 6:"C", 7:"A", 8:"R", 9:"Y"}
                MoveCursor(16, 6+i)
                print (color(word[i]))

        if signType == "grocery":
            for i in range(len("GROCERY")):
                word = {0:"G", 1:"R", 2:"O", 3:"C", 4:"E", 5:"R", 6:"Y"}
                MoveCursor(6+i, 40)
                print (color(word[i]))

        if signType == "weaponry":
            for i in range(len("WEAPONRY")):
                word = {0:"W", 1:"E", 2:"A", 3:"P", 4:"O", 5:"N", 6:"R", 7:"Y"}
                MoveCursor(36+i, 19)
                print (color(word[i]))       
        
        if signType == "armory":
            for i in range(len("ARMORY")):
                word = {0:"A", 1:"R", 2:"M", 3:"O", 4:"R", 5:"Y"}
                MoveCursor(33+i, 48)
                print (color(word[i]))