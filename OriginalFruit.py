

import os
import random
import GameBoard
from MyUtilities import *
from hud import *
from locations import *

class Fruit:
    #numFruit = 0
    def __init__(self, type, color = "red", seeds = 1, texture = "Smooth", weight = 1):
        self.type = type
        self.color = color
        self.seeds = seeds 
        self.texture = texture 
        self.weight = weight 
        self.ripe = False
        self.age = 0
        self.fallen = False
        

    def grow(self):
        chance = random.randint(1,6)
        if chance == 1:
            self.seeds += 1
        self.weight += random.randint(1,3)
        self.age+= 1
        if self.seeds >= 4:
            self.ripe = True
        if self.ripe:
            chance = random.randint(1,4)
            if chance == 1:
                self.fallen = True
                return self.seeds
        return 0


    def __str__(self):
        returnString = ""
        returnString += "Age: " + str(self.age) + "\n"
        returnString += "Seeds: " + str(self.seeds) + "\n"
        returnString += "Weight: " + str(self.weight) + "\n"
        returnString += "Ripe: " + str(self.ripe) + "\n"
        return returnString
        

class FruitTree:
    def __init__(self, type = "Apple", symbol = "^", fruits = 0):
        self.fruitList = []
        self.type = type
        self.age = 0
        self.symbol = symbol
        self.foreColor = "brown"
        self.backColor = "green"
        for i in range(fruits):
            self.fruitList.append(Fruit(self.type))

    def grow(self):
        self.age += 1
        #chance to grow new fruit
        chance = random.randint(1,10)
        if chance == 1:
            self.fruitList.append(Fruit(self.type))
        #for each fruit, capture number of seeds from each fruit
        totalSeeds = 0
        for f in self.fruitList:
            totalSeeds += f.grow()
        #capture onle fruit that has not fallen using "list comprehension"
        self.fruitlist = [f for f in self.fruitList if f.fallen == False]
        return totalSeeds    
    
    def __str__(self):
        returnString = self.type + " Tree   Age: "+str(self.age)+"\n"
        for f in self.fruitList:
            returnString += str(f) + "\n"
        return returnString
"""
while True: 
    os.system('cls')
    print(apple)
    apple.grow()
    input()
"""
class Orchard:
    def __init__(self, user1):
        #self.user1 = user1
        self.trees = {}
        self.board = GameBoard.Board()
        self.board.CreateBoard("Orchard", "#")
        #plant tree by setting occupied to tree and symbol to tree symbol. 

    def plantTree(self,row, col, type):
        if type not in self.trees:
            self.trees[type] = []
        newTree = FruitTree(type)
        self.trees[type].append(newTree)
        self.board.boardSize[row][col].description = newTree 
        self.board.boardSize[row][col].occupied = "newTree" 
        #self.board.boardSize[row][col].symbol = "^" 
        return newTree       

    def grow(self):
        for treeType in self.trees:
            for tree in self.trees[treeType]:
                seeds = tree.grow()
                for i in range(seeds):
                    chance = random.randint(1,5)
                    if chance == 1:
                        self.plantTree(treeType)
            
    def viewOrchard(self):
        self.board.ShowBoard()
        Hud.OrchardHud()

    def EnterOrchard(self):
        typeInput = "Apple"
        ClearScreen()
        self.viewOrchard()
        row, col = 1, 1

        #handle player trying to go off board!!!
        VALID_INPUTS = ["W","A","S","D","P","T","I","0"]
        while True:
            MoveCursor(row, col)
            #print ("O", end="", flush = True)
            self.board.boardSize[row][col].occupied = "player"
            self.board.boardSize[row][col].symbol = "O"
            self.board.boardSize[row][col].foreColor = "yellow"
            self.board.boardSize[row][col].backColor = "sienna4"
            self.board.boardSize[row][col].DisplayTile()
            while True:
                userInput = chr(GetKey()).upper()
                if userInput in VALID_INPUTS:
                    break
            newRow, newCol = row, col
            if userInput == "W":
                newRow -= 1
            elif userInput == "S":
                newRow += 1
            elif userInput == "A":
                newCol -= 1
            elif userInput == "D":
                newCol += 1
            elif userInput == "P":
                self.plantTree(row, col, typeInput)
                #self.board.boardSize[row][col].DisplayTile()
                continue
            elif userInput == "I":
                ClearScreen()
                if self.board.boardSize[row][col].occupied != None:
                    print (self.board.boardSize[row][col].description)  
                else:
                    print ("There is no tree here. ")         
                input()
                ClearScreen()
                self.viewOrchard()
                MoveCursor(row,col)
                #print("X",end="")
                self.board.boardSize[newRow][newCol].occupied = "player"
                continue 
            elif userInput == "T":
                ClearScreen()
                typeInput = input("Enter type of seed to start planting: ")
                ClearScreen()
                self.viewOrchard()
                MoveCursor(row,col)
                #print("X",end="")
                self.board.boardSize[row][col].occupied = "newTree"
                continue 
            elif userInput == "0":
                return "exit"
           
            MoveCursor(row,col)
            if self.board.boardSize[row][col].occupied == "player": 
                self.board.boardSize[row][col].occupied = None                   
                self.board.boardSize[row][col].foreColor = "chartreuse4" 
                self.board.boardSize[row][col].symbol = "#" 
            elif self.board.boardSize[row][col].occupied == "newTree":
               self.board.boardSize[row][col].foreColor = "green"
               self.board.boardSize[row][col].symbol = "^"                  
            self.board.boardSize[row][col].DisplayTile()  

            MoveCursor(newRow,newCol)            
            self.board.boardSize[newRow][newCol].occupied = "player"
            self.board.boardSize[newRow][newCol].foreColor = "yellow" 
            self.board.boardSize[newRow][newCol].DisplayTile()
            row, col = newRow, newCol
"""
def main():
    orchard = Orchard()
    typeInput = input("Enter the type of tree to plant to get started: ").upper()
    orchard.plantTree(typeInput)

    while True:
        os.system('cls')
        orchard.grow()
        orchard.viewOrchard()
        userInput = input("(P)lant a tree or any key to continue. ").upper()
        if userInput == "P":
            typeInput = input("Enter the type of tree to plant: ").upper()
            orchard.plantTree(typeInput)
"""      
"""
        treeNum = 1
        for treeType in self.trees:
            for tree in self.trees[treeType]:
                #notice how i used tree.age instead of self.age
                print("Tree #"+str(treeNum)+" Age: "+str(tree.age))
                print ("Tree Type: "+ tree.type)
                print(tree)
                input()
                os.system('cls')
                treeNum += 1
                """