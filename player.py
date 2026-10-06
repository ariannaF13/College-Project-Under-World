"""
Arianna Ford
2022_01_30
Player
"""
import random
from MyUtilities import *
from color_extractor import *
from GameBoard import *
from OriginalFruit import *
from hud import *
from locations import *
import math

class Game_Character:
    def __init__(self, attack, defense, health):
        #player stats
        self.attack = DieRoller(3,6)
        self.defense = DieRoller(2,6)   
        self.floorLevel = 0
        self.health = 100
        self.name = Game_Character.genPlayerName()
        self.inventory = ["shield", "sword", "potion of strength"]
        self.activatedInventory = []
        self.gold = 10

        #count for times each item has been used
        self.potHeal = 0
        self.potStr = 0
        self.potUnk = 0
        self.potSte = 0
        self.apple = 0
        self.salt = 0
        self.bloss = 0
        self.sword = 0
        self.cloak = 0
        self.helmet = 0
        self.chest = 0
        self.shield = 0

    #generating player name
    def genPlayerName():
        gender = random.randint(1,2)
        if gender == 1:
            firstNameSyl1 = [ "Farr", "Delil", "Dor", "Ada", "Ani", "Clar", "Emi", "Bel", "Kri", "Jul", "Mad", "Tin", "Jes", "Shaw", "Beck", "Quin", "Ana", "Dork", "Ed", "Ru",
            "Paul"] 
            firstNameSyl2 = ["la", "ah", "lee", "line", "uh", "er", "ice", "tsy" "ael", "sty", "ie", "in", "ith", "ecy", "stasia", "us", "by", "sor", "row", "ine","ia", "e"]
            middleName = ["Rylee", "Lenae", "James", "Allen", "Liam", "Ronald", "Oliver", "Rhed", "Lucas", "Henry", "Quinn"]
            lastName = ["Pauly", "Smith", "Miller", "Jones", "Broun", "Welsh", "Ruth", "Roosevelt", "Eastwood", "Lynam", "Browning", "Garfield", "Blackmoore",
            "Adington", "Wellington", "Berrow", "Beswick", "Everly", "Shoemocker"]
            playerFullName = (firstNameSyl1[random.randint(0,len(firstNameSyl1)-1)] + firstNameSyl2[random.randint(0,len(firstNameSyl2)-1)] + " " + middleName[random.randint(0,len(middleName)-1)] + " " + lastName[random.randint(0,len(lastName)-1)])
            return playerFullName
        #male name generated below  
        elif gender == 2:
            firstNameSyl1 = [ "Farr", "Spenc", "Mich", "Kri", "Jes", "Shaw", "Beck", "Dork", "Ed", "Ru", "Wind",
            "Wood", "Paul", "Abra", "Bald", "Ald", "Al", "Bron"] 
            firstNameSyl2 = ["uh", "er", "ael", "ie", "in", "ith", "us", "ward", "by", "sor", "row", "ine", "ham", "ston", "win", "red", "son"]
            middleName = ["Rylee", "Lenae", "James", "Allen", "Liam", "Ronald", "Oliver", "Rhed", "Lucas", "Henry", "Quinn"]
            lastName = ["Pauly", "Smith", "Miller", "Jones", "Broun", "Welsh", "Ruth", "Roosevelt", "Eastwood", "Lynam", "Browning", "Garfield", "Blackmoore",
            "Adington", "Wellington", "Berrow", "Beswick", "Everly", "Shoemocker"]
            playerFullName = (firstNameSyl1[random.randint(0,len(firstNameSyl1)-1)] + firstNameSyl2[random.randint(0,len(firstNameSyl2)-1)] + " " + middleName[random.randint(0,len(middleName)-1)] + " " + lastName[random.randint(0,len(lastName)-1)])
            return playerFullName

class Actors:
    def __init__(self, row, col, symbol, foreColor):        
        self.row = row
        self.col = col
        self.newRow = 0
        self.newCol = 0
        self.symbol = symbol
        self.foreColor = foreColor
        self.backColor = "gray20" 
        self.pastMoves = []  

    def PlaceActor(self, board, foreColor, actorType, boardType): #creating cordinates for player
        if boardType == "market":
            self.row = 48
            self.col = 27
            board.boardSize[self.row][self.col].backColor = "darkolivegreen" #makinf player placesment in market static
        else:
            if actorType == "player": #separates spawn point from enemies in dungeon
                    roomChoice = 0
            elif actorType == "monster":
                roomChoice = random.randint(1,9)
            while True:        
                self.row = (board.midpointList[roomChoice][0])
                self.col = (board.midpointList[roomChoice][1])
                if board.boardSize[self.row][self.col].occupied == None:
                    break
                else:
                    self.row+1
                    self.col-1
                    break
            board.boardSize[self.row][self.col].backColor = "gray20"
        MoveCursor(self.row, self.col) 
        board.boardSize[self.row][self.col].occupied = actorType
        board.boardSize[self.row][self.col].foreColor = foreColor #placing player

    def ItemUse(self): #allowing player to activate items
        attackIncrease = 0
        healthIncrease = 0
        defenseIncrease = 0
        #test to see if item is in activated list and if its been activated to prevent compound
        #this occurs for ever item
        if "potion of health" in self.activatedInventory: 
            self.potHeal +=1
            if self.potHeal == 3: 
                self.activatedInventory.remove("potion of health")
                self.potHeal = 0
            elif self.potHeal == 2:
                healthIncrease += 10
            else:
                pass
        
        if "potion of strength" in self.activatedInventory:
            self.potStr +=1
            if self.potStr == 7:
                self.activatedInventory.remove("potion of strength")
                attackIncrease -= 6
                self.potStr = 0
            elif self.potStr == 2:
                attackIncrease += 6
            else:
                pass

        if "potion of unknown" in self.activatedInventory:
            self.potUnk +=1
            if self.potUnk == 10:
                self.activatedInventory.remove("potion of unknown")
                defenseIncrease -= 7
                attackIncrease +=2
                self.potUnk = 0
            elif self.potUnk == 2:
                defenseIncrease += 7
                attackIncrease -=2
            else:
                pass

        if "apple" in self.activatedInventory:
            self.apple+=1
            if self.apple == 2:
                self.activatedInventory.remove("apple")
                self.apple = 0
            else:
                healthIncrease +=5

        if "pheonix blossom" in self.activatedInventory:
            self.bloss +=1
            if self.bloss == 15:
                self.activatedInventory.remove("pheonix blossom")
                attackIncrease -= 7
                self.bloss = 0
            elif self.bloss == 2:
                attackIncrease += 10
            else:
                pass
            
        if "sword" in self.activatedInventory:
            self.sword +=1
            if self.sword == 40:
                self.activatedInventory.remove("sword")
                attackIncrease -= 5
                self.sword = 0
            elif self.sword == 2:
                attackIncrease +=5
            else:
                pass
        if "obsidian sword" in self.activatedInventory:
            self.sword +=1
            if self.sword == 70:
                self.activatedInventory.remove("pbsidian sword")
                attackIncrease -= 5
                self.sword = 0
            elif self.sword == 2:
                attackIncrease +=9
            else:
                pass

        if "helmet" in self.activatedInventory:
            self.helmet += 1
            if self.helmet == 60:
                self.activatedInventory.remove("helmet")
                defenseIncrease -= 3
                self.helmet = 0
            elif self.helmet == 2:
                defenseIncrease +=3
            else:
                pass
        
        if "chestplate" in self.activatedInventory:
            self.chest += 1
            if self.chest == 55:
                self.activatedInventory.remove("chestplate")
                defenseIncrease -=5
                self.chest = 0
            elif self.chest == 2:
                defenseIncrease +=7
            else: pass

        if "shield" in self.activatedInventory:
            self.shield += 1
            if self.shield == 50:
                self.activatedInventory.remove("shield")
                defenseIncrease -= 4
                self.shield = 0
            elif self.shield == 2:
                defenseIncrease +=5
            else:
                pass
            
        self.attack +=attackIncrease
        self.defense +=defenseIncrease
        while True: #test to see if player health is already at 100
            test = self.health+healthIncrease
            if test >= 100:
                healthIncrease-=1
                continue
            else:
                self.health+=healthIncrease
                break
        self.health +=healthIncrease
        MyUtilities.MoveCursor(9,62) #clear past stats
        print (" "*14)
        MyUtilities.MoveCursor(10,62)
        print (" "*14)
        MyUtilities.MoveCursor(11,62)
        print (" "*14)
        MyUtilities.MoveCursor(9,62)#display updated stats
        print (term.yellow("Attack: "+str(self.attack)),flush=True)
        MyUtilities.MoveCursor(10,62)
        print (term.yellow("Defense: "+str(self.defense)), flush=True)
        MyUtilities.MoveCursor(11,62)
        print (term.yellow("Health: "+str(self.health)), flush=True)

    def ActivatedCheck(self): #allowing player to activate item
        while True:
            MoveCursor(37, 62)
            print ("What item would you like to activate? ")
            MoveCursor(38, 62)
            print ("(E)xit")
            if self.inventory == 0: #testing if player has anything to activate
                break
            for l in range(10): #clearing past inventory
                MoveCursor(39+l, 62)
                print (" "*35)
            for i in range(len(self.inventory)): #displaying updated inventory
                MoveCursor(39+i, 62)
                print (term.orange("("+str(i)+")"+str(self.inventory[i]))) 
            
            userChoice = chr(GetKey()).upper()            
            if userChoice == "E":#exiting activation menu and reseting menu
                MoveCursor(37, 62)
                print (" "*37)
                MoveCursor(38, 62)
                print (" "*37)
                for l in range(10):
                    MoveCursor(39+l, 62)
                    print (" "*35)
                break
            try: 
                userChoice = int(userChoice)
                if userChoice >= (len(self.inventory)): #testing to see if user choice can be activates
                    break
            except ValueError:
                continue
            else:
                if userChoice>(len(self.inventory)):
                    continue
                else:
                    self.activatedInventory.append(self.inventory.pop(userChoice)) #removing item from inventory to be activated and display
                    startPoint = 50-(len(self.activatedInventory))
                    for i in range(len(self.activatedInventory)):
                        for l in range(11):
                            MoveCursor(39+l, 62)
                            print (" "*35)
                        MoveCursor(startPoint+i, 62)
                        print (term.green(self.activatedInventory[i]))
                        continue

    def InventoryCheck(self): #making sure user inventory is not too large
        while True:
            if len(self.inventory)==10:  
                for l in range(12):
                    MoveCursor(37+l, 62)
                    print (" "*35)
                MoveCursor(37, 62)
                print (term.red("There is too much in your inventory. "))
                for i in range(len(self.inventory)):
                    print (term.orange("("+str(l)+")"+str(self.inventory[l]))) 
                while True:
                    userChoice = chr(GetKey()).upper()
                    if userChoice == "E":
                        break
                    try: 
                        userChoice = int(userChoice)
                        if userChoice <= (len(self.inventory)):
                            break
                    except ValueError:
                        continue
                userChoice = input().upper()
                for l in range(12):
                    MoveCursor(37+l, 62)
                    print (" "*35)
                MoveCursor(37, 62)
                print (term.red("You are getting rid of: "+str(self.inventory[userChoice]))) #letting user discard items
                MoveCursor(38, 62)
                userCheckChoice = input("Are you sure? (Y/N)").upper() #double checking
                if userCheckChoice == "Y":
                    self.inventory.pop(userChoice)
                    continue
                elif userCheckChoice == "N":
                    continue
                else:
                    MoveCursor(38, 62)
                    print ("Invalid input. ")
                    continue

            else:
                for l in range(len(self.inventory)): #redisplaying inventory
                    MoveCursor(36+l, 62)
                    print (" "*35)
                MoveCursor(36, 62)
                print("User Inventory: ")
                for l in range(len(self.inventory)):
                    MoveCursor(39+l, 62)
                    print (term.orange(self.inventory[l])) #separating activates and unactivated by color
                startPoint = 50-(len(self.activatedInventory))
                for i in range(len(self.activatedInventory)):
                    MoveCursor(startPoint+i, 62)
                    print (term.green(self.activatedInventory[i]))
                break
                    

    def MoveActor(self, board, dungeonHud, foreColor, user1, userMove, actorType, monster): #moving player on board
        VALID_INPUTS = ["W", "A", "S", "D", "0", "V", "I"] 
        while True:
            if userMove in VALID_INPUTS: #test inputs
                break
            else:
                dungeonHud._message.append("Please enter a valid input. ")
                dungeonHud.colorsList.append("red")
                dungeonHud.SystemMessage()
                return "continue"

        #resetting row and col  
        #testing to make sure player doesnt walk off board
        #same for each direction
        self.newRow, self.newCol = self.row, self.col             
        if userMove == "W":     
            if board.boardSize[self.row-1][self.col].symbol == "#": 
                dungeonHud.SystemMessage()
                return "wallMessage"
            if board.boardSize[self.row-1][self.col].occupied == "monster":    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud) 
            else:                                        
                self.newRow -=1                


        elif userMove == "S":                
            if board.boardSize[self.row+1][self.col].symbol == "#":
                dungeonHud.SystemMessage()
                return "wallMessage"
            if board.boardSize[self.row+1][self.col].occupied == "monster":    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud)  
            else:                    
                self.newRow +=1                


        elif userMove == "A":
            if board.boardSize[self.row][self.col-1].symbol == "#":
                dungeonHud.SystemMessage()
                return "wallMessage"
            if board.boardSize[self.row][self.col-1].occupied == "monster":    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud)  
            else:                    
                self.newCol -=1                
        

        elif userMove == "D":
            if board.boardSize[self.row][self.col+1].symbol == "#":
                dungeonHud.SystemMessage()
                return "wallMessage"
            if board.boardSize[self.row][self.col+1].occupied == "monster":
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud)  
            else:                    
                self.newCol +=1 

        elif userMove == "0": #exiting dungeon
            return "exit" 
        elif userMove == "V": #viewing player
            for i in range(7):
                MoveCursor(22+i, 62)
                print (" "*35)
            MoveCursor(22, 62)
            print (term.green("Name: "+str(user1.name)))
            MoveCursor(23,62)
            print (term.green(user1.history))
            MoveCursor(24,62)
            print (term.green("Attack: "+str(user1.attack)))
            MoveCursor(25, 62)
            print (term.green("Defense: "+str(user1.defense)))
            input()
            for i in range(7):
                MoveCursor(22+i, 62)
                print (" "*35)
        elif userMove == "I": #allowing player to activate items
            self.ActivatedCheck()
            return "continue"

                    

        #changing old tile to floor tile for dungeon
        MoveCursor(self.row,self.col)
        if board.boardSize[self.row][self.col].occupied == "player" or "monster":
            board.boardSize[self.row][self.col].occupied = None
            board.boardSize[self.row][self.col].description = " "
        board.boardSize[self.row][self.col].passable = True
        
        #making modifactions to past tile for market
        if monster  == "market":
            board.boardSize[self.row][self.col].backColor = "darkolivegreen"
            board.boardSize[self.row][self.col].foreColor = "palegreen4"
            if board.boardSize[self.row][self.col].doorHere == True:
                board.boardSize[self.row][self.col].foreColor = "darkorange4"
        else:
            board.boardSize[self.row][self.col].backColor = "gray20"
            board.boardSize[self.row][self.col].foreColor = "gray25"

        #test stairs to make sure stairs go back to original color
        if board.boardSize[self.row][self.col].stairsHere == True:
            board.boardSize[self.row][self.col].symbol = "<"
            board.boardSize[self.row][self.col].foreColor = "black"
        board.boardSize[self.row][self.col].DisplayTile()

        #changing new tile to player     
        MoveCursor(self.newRow,self.newCol)
        board.boardSize[self.newRow][self.newCol].passable = False
        board.boardSize[self.newRow][self.newCol].occupied = actorType
        if actorType == 'monster':
            board.boardSize[self.newRow][self.newCol].description = monster
        board.boardSize[self.newRow][self.newCol].foreColor = foreColor
        if monster  == "market":
            board.boardSize[self.newRow][self.newCol].backColor = "darkolivegreen"
        else:
            board.boardSize[self.newRow][self.newCol].backColor = "gray20"
        board.boardSize[self.newRow][self.newCol].DisplayTile() 
        if foreColor == "yellow":
            user1.steps +=1
        self.row, self.col = self.newRow, self.newCol
        if board.boardSize[self.newRow][self.newCol].potion == True:
            board.boardSize[self.newRow][self.newCol].potion = False
            board.boardSize[self.newRow][self.newCol].foreColor = "gray25"
            return "potionMessage"
        if board.boardSize[self.newRow][self.newCol].stairsHere == True:
            return "stairsMessage"
        

class Player(Game_Character, Actors):
    def __init__(self, row, col, symbol, foreColor, attack, defense, health):
        Game_Character. __init__(self, attack, defense, health)
        Actors. __init__(self, row, col, symbol, foreColor)
        self.xpValue = 0
        self.level = 0
        self.steps = 0
        self.history = Player.GenPlayerHistory()
        
    def GenPlayerHistory(): #creating story for player, had to be shortened to be propperly displayed
        experience = ["sadness", "hate", "revenge", "searching", "love", "happiness", "anger", "beggars", "traveling", "travelers", "schooling", "training", "research", 
        "creating", "mourning"]
        makeMoney = ["stealing", "knitting", "dueling", "gambling", "baking", "trading", 
        "cleaning", "washing clothes", "bartending", "making candles"]
        learned = ["fight", "survive", "read", "hunt", "cook", "clean", "speak"]
        fam = ["your mom", "your dad", "your grandma", "your pawpaw", "your uncle", "your aunt", "your sister", "your brother", "your cousin", "a family friend", "the neighbor"]
        
        #year = (random.randint(1800,1930))
        playerHist = ("You make money by "+makeMoney[random.randint(0,len(makeMoney)-1)]+".")
        #life is full of "+experience[random.randint(0,len(experience)-1)]+
        #+" you learned to "+learned[random.randint(0,len(learned)-1)]+" from "+fam[random.randint(0,len(fam)-1)]+". ")
        return playerHist        
    #history = GenPlayerHistory() 

    def Interact(self, monster, board, dungeonHud): #allow user to interact
        healthDecrease = self.attack - monster.defense #attack enemy
        while True:
            if healthDecrease <=0:
                healthDecrease+=1
                continue
            else:
                break
        monster.health -= healthDecrease       
        dungeonHud._message.append("You attack the enemy, their health goes down by "+str(healthDecrease))
        dungeonHud.colorsList.append("yellow")
        dungeonHud.SystemMessage()
        MoveCursor(22, 62)#clearing screen of enemy stats and updating them
        print (" "*15)
        MoveCursor(23,62)
        print (" "*15)
        MoveCursor(24,62)
        print (" "*15) 
        MoveCursor(22, 62)
        print (term.red("Attack: "+str(monster.attack)))
        MoveCursor(23,62)
        print (term.red("Defense: "+str(monster.defense)))
        MoveCursor(24,62)
        print (term.red("Health: "+str(monster.health)))
    def death():
        pass



class Monster(Game_Character, Actors): #basic enemy
    def __init__(self, row, col, symbol, foreColor, attack, defense, health):
        Game_Character. __init__(self, attack, defense, health)
        Actors. __init__(self, row, col, symbol, foreColor)
        self.attack = 6
        self.health = 50
        self.xpValue = 0
        self.monsterType = ""

    def Interact(self, dungeonHud, actorType): #basic enemy interaction, just growl
        if actorType == "monster":
            pass
        elif actorType == "player":
            dungeonHud._message.append("The monster growls at you...")
            dungeonHud.colorsList.append("red3")

    def Death(self, dungeonHud, board, monsterNum, x): #enemy death
        dungeonHud._message.append("You defeated the Monster. ")
        dungeonHud.colorsList.append("yellow")
        monsterNum.pop(x)
        board.boardSize[self.row][self.col].occupied = None
        
class Demon(Monster): #demon enemy
    def __init__(self, row, col, symbol, foreColor, attack, defense, health):
        Monster. __init__(self, row, col,symbol, foreColor, attack, defense, health)
        self.health = 50
        self.symbol = symbol
        self.foreColor = foreColor
        self.teleportAbility = True
        self.posessed = False
        self.messageInfoNum = 0
        self.moveNum = 0
        self.chance = random.randint(5,300)
        self.moveList = {0:0, 1:0, 2:0, 3:0}
        self.areaMessage = False

    def MoveActor(self, board, dungeonHud, foreColor, user1, userMove, actorType, monster):
        self.newRow, self.newCol = self.row, self.col  
        #testing movement here and letter being passed in, can be random or not 
        # for each direction, test for wall, which type of interaction and finall change row or col             
        if userMove == "W":  
            if board.boardSize[self.row-1][self.col].symbol == "#":
                return "continue"
            if board.boardSize[self.row-1][self.col].occupied != None:    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud)  
            else:                                        
                self.newRow -=1                

        elif userMove == "S":                
            if board.boardSize[self.row+1][self.col].symbol == "#":
                return "continue"
            if board.boardSize[self.row+1][self.col].occupied != None:    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud) 
            else:                    
                self.newRow +=1                

        elif userMove == "A":
            if board.boardSize[self.row][self.col-1].symbol == "#":
                return "continue"
            if board.boardSize[self.row][self.col-1].occupied != None:    
                if actorType == "monster":
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud) 
            else:                    
                self.newCol -=1                
        
        elif userMove == "D":
            if board.boardSize[self.row][self.col+1].symbol == "#":
                return "continue"
            if board.boardSize[self.row][self.col+1].occupied != None:
                if actorType == "monster":
                    actorType = board.boardSize[self.row][self.col+1].occupied
                    monster.Interact(dungeonHud, actorType, user1)
                elif actorType == "player":
                    user1.Interact(monster, board, dungeonHud)  
            else:                    
                self.newCol +=1  
        elif userMove == "0":
            return "exit" 
        elif userMove == "teleport": #allowing demon to teleport when health is low
            while True:
                self.newRow = random.randint(10,40)
                self.newCol = random.randint(10,50)
                if board.boardSize[self.newRow][self.newCol].foreColor != "gray25":
                    continue
                else:
                    monster.teleportAbility = False
                    monster.foreColor = "red"
                    break
                    

        #changing old tile to floor tile
        MoveCursor(self.row,self.col)
        if board.boardSize[self.row][self.col].occupied == "player" or "monster":
            board.boardSize[self.row][self.col].occupied = None
            board.boardSize[self.row][self.col].description = " "
        board.boardSize[self.row][self.col].passable = True
        board.boardSize[self.row][self.col].foreColor = "gray25"
        board.boardSize[self.row][self.col].backColor = "gray20"
        #test stairs to make sure stairs go back to original color
        if board.boardSize[self.row][self.col].stairsHere == True:
            board.boardSize[self.row][self.col].symbol = "<"
            board.boardSize[self.row][self.col].foreColor = "black"
        board.boardSize[self.row][self.col].DisplayTile()  

        #changing new tile to player     
        MoveCursor(self.newRow,self.newCol)
        board.boardSize[self.newRow][self.newCol].passable = False
        board.boardSize[self.newRow][self.newCol].occupied = actorType
        if actorType == 'monster':
            board.boardSize[self.newRow][self.newCol].description = monster
        board.boardSize[self.newRow][self.newCol].foreColor = foreColor
        board.boardSize[self.newRow][self.newCol].backColor = "gray20"
        board.boardSize[self.newRow][self.newCol].DisplayTile() 
        if foreColor == "yellow":
            user1.steps +=1
        self.row, self.col = self.newRow, self.newCol
        if board.boardSize[self.newRow][self.newCol].stairsHere == True:
            return "stairsMessage"


    def MonsterMove(self, board, monsterNum, x, dungeonHud, user1, areaTest):#demon movement generated here
        if self.health <= 15 and self.teleportAbility == True:     #transportation is called here  
            monsterNum[x].MoveActor(board, dungeonHud, 'black', user1, "teleport", 'monster', monsterNum[x]) 
        elif self.teleportAbility == False or self.health>15: #demon moving toward payer if player is close enough
            if areaTest == True:
                if user1.col == monsterNum[x].col: #col stays same
                    colDifference = 0                
                else:
                    colDifference = monsterNum[x].col - user1.col #assigning difference between cols to variable
                if user1.row == monsterNum[x].row: #row stays same
                    rowDifference = 0
                else:
                    rowDifference = monsterNum[x].row - user1.row#assigning difference between rows to variable
                rowcol = random.randint(0,1) #letting choice between moving row or col be random unless row or col match
                if colDifference == 0:
                    rowcol = 0
                elif rowDifference == 0:
                    rowcol = 1
                if rowcol == 0: #changing the row
                    if rowDifference <0:
                        monsterMove = "S"
                    else:
                        monsterMove = "W"
                elif rowcol == 1: #changing the col
                    if colDifference <0:
                        monsterMove = "D"
                    else:
                        monsterMove = "A"
            else: #otherwise demon movement is random
                randomMove = random.randint(0,3)
                if randomMove == 0:
                    monsterMove = "W"
                elif randomMove == 1:
                    monsterMove = "A"
                elif randomMove == 2:
                    monsterMove = "S"
                elif randomMove == 3:
                    monsterMove = "D"  
            monsterNum[x].MoveActor(board, dungeonHud, 'black', user1, monsterMove, 'monster', monsterNum[x]) 
            

    def posession(self, dungeonHud): #demon will posess you for 4 turns
        if self.posessed == True:
            pass
        else:
            self.moveList[0] = random.randint(0,3)
            self.moveList[1] = random.randint(0,3)
            self.moveList[2] = random.randint(0,3)
            self.moveList[3] = random.randint(0,3)
            dungeonHud._message.append("You have been posessed. ")
            dungeonHud.colorsList.append("red")
            dungeonHud.SystemMessage()
            self.posessed = True
            if self.moveNum <3:
                self.moveNum +=1
            else:
                self.moveNum = 0
            return self.moveList


    def AreaTest(self, user1, dungeonHud, monsterNum, x): #testing to see if player is close to demon or not
            xPoint = math.pow(user1.row - monsterNum[x].row, 2)
            yPoint = math.pow(user1.col - monsterNum[x].col, 2)
            distance = math.sqrt((xPoint)+(yPoint))
            if distance <= 7:
                self.areaMessage = True
                return True
            elif distance >7:
                self.areaMessage = False
                return False
        

    def Interact(self, dungeonHud, actorType, user1): #interaction of demon to others
        if actorType == "player": #attack player
            healthDecrease = self.attack - user1.defense
            while True:
                if healthDecrease <=0:
                    healthDecrease+=2
                    continue
                else:
                    break
            user1.health -= healthDecrease        
            dungeonHud._message.append("The enemy is attacking you, your health is down by: "+str(healthDecrease))
            dungeonHud.colorsList.append("red3")
            dungeonHud.SystemMessage()
            MyUtilities.MoveCursor(5,62)
            print (" "*14)
            MyUtilities.MoveCursor(11,62)
            print (term.yellow("Health: "+str(user1.health)))
        else: #if interaction is not with player, pass
            pass
    

    def Death(self, dungeonHud, board, monsterNum, x, user1): #demon dying
        moneyIncrease = random.randint(10,15)
        user1.gold += moneyIncrease #player gold increasing
        dungeonHud._message.append("You defeated the Demon. ")
        dungeonHud.colorsList.append("red3")
        dungeonHud.SystemMessage()
        monsterNum.pop(x)
        MoveCursor(22, 62) #cleating demon stats and removing it from dict
        print (" "*10)
        MoveCursor(23,62)
        print (" "*10)
        MoveCursor(24,62)
        print (" "*10) 
        MoveCursor(12,62)
        print ("Gold: " + str(user1.gold))
        board.boardSize[self.row][self.col].occupied = None
        board.boardSize[self.row][self.col].DisplayTile() 


class Spirit(Monster): #start of another enemy, only acts as alarm, passive
    def __init__(self, row, col, symbol, foreColor, defense, health):
        Monster. __init__(self, row, col,symbol, foreColor, defense, health)
    def AreaTest(self, user1, monsterNum, x):
        xPoint = math.pow(user1.row - monsterNum[x].row, 2)
        yPoint = math.pow(user1.col - monsterNum[x].col, 2)
        distance = math.sqrt((xPoint)+(yPoint))
        if distance <= 7:
            self.areaMessage = True
            return True
        elif distance >7:
            self.areaMessage = False
            return False
    def PlaceActor(self, board, foreColor, actorType):
        area = board.boardSize[board.midpointList[board.roomChoice][0]][board.midpointList[board.roomChoice][1]]
        spawnX = board.midpointList[board.roomChoice][0]
        spawnY = board.midpointList[board.roomChoice][1]
        while True:
            spawnX+=1
            if board.boardSize[spawnX][board.midpointList[board.roomChoice][1]+1].backColor != "black":
                continue
            else:
                break
        while True:
            spawnY+=1
            if board.boardSize[board.midpointList[board.roomChoice][0]][spawnY].backColor != "black":
                continue
            else:
                break
            #self.row = random.randint(10,40)
            #self.col = random.randint(10,50)
            #if board.boardSize[self.newRow][self.newCol].foreColor != "gray25":
                #continue