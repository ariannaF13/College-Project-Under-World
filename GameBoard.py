"""
Arianna Ford
2022_02_22
Game Board
"""
from MyUtilities import *
import math

class Tile(): #each individual tiles for board
    def __init__(self, foreColor, backColor, symbol = "#", passable = False, description = ""):
        self.symbol = symbol
        self.occupied = None
        self.foreColor = foreColor
        self.backColor = backColor
        self.contents = []
        self.passable = passable
        self.description = description
        self.stairsHere = False
        self.doorHere = False
        self.potion = False
        self.color = getattr(term, (self.foreColor+"_on_"+self.backColor))
        
    def DisplayTile(self): #actually prints tile object, pritorizes which tile is on top. 
        fc = self.foreColor
        bc = self.backColor
        color = getattr(term, fc+"_on_"+bc)
        if self.occupied == "player":
            self.symbol = "O"
        elif self.occupied == "monster":
            self.symbol = "¤"
        elif self.occupied == "newTree":
            self.symbol = "^"
        elif self.potion == True:
            self.symbol = "!"    
        elif self.stairsHere == True:
            self.symbol = "<" 
        elif self.doorHere == True:
            self.symbol = "+"           
        elif self.passable == True:
            self.symbol = "."
        
        
        print(color(self.symbol), end="", flush = True)
             

    
        


class Board():
    def __init__(self):
        self.midpointList = []
        self.roomChoice = random.randint(4,9) #choosing random room
        self.colLen = 60 #width
        self.rowLen = 51 #height
        self.boardSize = []

    def PlacePotion(self): #placing random potion on each board
        while True:
            row = random.randint(10,40)
            col = random.randint(10,50)
            if self.boardSize[row][col].foreColor != "gray25":
                continue
            else:
                break
        self.boardSize[row][col].foreColor = "green"
        self.boardSize[row][col].potion = True

    def CreateBoard(self,boardType,symbol): #creates board, recognizing which type of board to use different colors
        for i in range(int(self.rowLen)-1):
            self.boardSize.append([])
            for j in range(int(self.colLen)-1):
                if boardType == "Orchard":
                    backColor = "sienna4"
                    colorChoice = random.randint (1,4)
                    if colorChoice == 1:
                        foreColor = "green3"
                    elif colorChoice == 2:
                        foreColor = "webgreen"
                    elif colorChoice == 3:
                        foreColor = "green4"
                    elif colorChoice == 4:
                        foreColor = "darkolivegreen4"
                elif boardType == "Dungeon":
                    foreColor = "gray17"
                    backColor = "gray9"
                elif boardType == "yard":
                    foreColor = "palegreen4"
                    backColor = "darkolivegreen"
                (self.boardSize[i].append(Tile(foreColor, backColor, symbol)))
        return self.boardSize

    
    def CreateRooms(self, amount, boardType): #creating room cordinates      
        for i in range(amount):
            if boardType == "yard": #if the board is the market, will be making building cordinates instead of rooms
                #top left
                if i == 0:
                    col = 3
                    row = 2
                    width = 16
                    height = 17
                #top right
                elif i == 1:  #first part of L shape room
                    col = 40
                    row = 3
                    width = 19
                    height = 17
                #bottom left
                elif i == 2:
                    col = 2
                    row = 32
                    width = 17
                    height = 19
                #bottom right
                elif i == 3:
                    col = 48
                    row = 30
                    width = 12
                    height = 10
                elif i == 4:  #L shape of room
                    col = 35
                    row = 16
                    width = 6
                    height  = 6

            else:
                while True: #otherwise, making room cordinates in dungeon
                    col = random.randint(3,45)
                    row = random.randint(3,35)
                    width = random.randint(7,12)
                    height = random.randint(7,10)
                    relativeWidth = col + width
                    relativeHeight = row + height
                    maxWidth = 45
                    maxHeight = 35
                    if relativeWidth >= maxWidth: #making sure room cordinate sizes are not too large
                        if relativeHeight >= maxHeight:
                            continue
                    else:
                        break
            self.MakeRoom(col, row, width, height, boardType)
    
    def MakeRoom(self, col, row, width, height, boardType): #displaying the rooms/buildings with proper colors and symbols
        midpointY = (math.trunc((width)/2)+col)-1
        midpointX = (math.trunc((height)/2)+row)-1
        self.midpointList.append([midpointX,midpointY]) #creating midpoint list

        for i in range(width-1):
            for l in range(height-1):
                if boardType == "yard": #market
                    self.boardSize[row+i][col+l].symbol = "#" 
                    self.boardSize[row+i][col+l].passable = False
                    self.boardSize[row+i][col+l].foreColor = "darkorange4"
                    self.boardSize[row+i][col+l].backColor = "orange4" 
                else:   #dungeon
                    self.boardSize[row+i][col+l].symbol = "."
                    self.boardSize[row+i][col+l].passable = True
                    self.boardSize[row+i][col+l].foreColor = "gray25"
                    self.boardSize[row+i][col+l].backColor = "gray20"
        

    def BuildCorridors(self): #building corridors for dungeon
        for i in range(len(self.midpointList)-1):
            
            firstRoomX = int(self.midpointList[i][0])
            secondRoomX = int(self.midpointList[i+1][0])
            #print(firstRoomX, secondRoomX)
            if firstRoomX < secondRoomX:                
                for j in range(self.midpointList[i][0], self.midpointList[i+1][0]):                                      
                    self.boardSize[j][self.midpointList[i][1]].symbol = "."
                    self.boardSize[j][self.midpointList[i][1]].passable = True
                    self.boardSize[j][self.midpointList[i][1]].foreColor = "gray25"
                    self.boardSize[j][self.midpointList[i][1]].backColor = "gray20"                                      
       
            else:
                for j in range(self.midpointList[i][0], self.midpointList[i+1][0], -1):
                    self.boardSize[j][self.midpointList[i][1]].symbol = "."
                    self.boardSize[j][self.midpointList[i][1]].passable = True
                    self.boardSize[j][self.midpointList[i][1]].foreColor = "gray25"
                    self.boardSize[j][self.midpointList[i][1]].backColor = "gray20"
     
            #left right below:
            firstRoomY = self.midpointList[i][1]
            secondRoomY = self.midpointList[i+1][1]
            if firstRoomY < secondRoomY:
                for l in range(self.midpointList[i][1], self.midpointList[i+1][1]):
                    self.boardSize[j][l].symbol = "."
                    self.boardSize[j][l].passable = True
                    self.boardSize[j][l].foreColor = "gray25"
                    self.boardSize[j][l].backColor = "gray20"
      
            else:
                for l in range(self.midpointList[i][1], self.midpointList[i+1][1],-1):
                    self.boardSize[j][l].symbol = "."
                    self.boardSize[j][l].passable = True
                    self.boardSize[j][l].foreColor = "gray25"
                    self.boardSize[j][l].backColor = "gray20"
                    
    def PlaceStairs(self): #randomly placing stairs
        self.boardSize[self.midpointList[self.roomChoice][0]][self.midpointList[self.roomChoice][1]].stairsHere = True      
        self.boardSize[self.midpointList[self.roomChoice][0]][self.midpointList[self.roomChoice][1]].foreColor = "black"      
        self.boardSize[self.midpointList[self.roomChoice][0]][self.midpointList[self.roomChoice][1]].backColor = "gray20"  
       

    def ShowBoard(self): #displaying board. 
        MoveCursor(0,0)
        for row in range (len(self.boardSize)):            
            for col in range(len(self.boardSize[row])):
                self.boardSize[row][col].DisplayTile()
            print ()
