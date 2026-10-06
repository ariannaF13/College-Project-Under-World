"""
Arianna Ford
02_28_2022
HUD Class
"""
import MyUtilities 
from MyUtilities import *

class Hud:
    def __init__(self):
        self._message = []
        self.colorsList = []

    def DrawHud(self, backColor, foreColor, row, col, startingPoint_row, startingPoint_col): #making basic HUD outline, parameters allow you to make different sizes
        backColor = backColor
        foreColor = foreColor
        row = int(row)
        col = col
        startingPoint_row = startingPoint_row
        startingPoint_col = startingPoint_col       
        MyUtilities.MoveCursor(startingPoint_row, startingPoint_col)
        MyUtilities.MoveCursor(startingPoint_row, startingPoint_col)
        
        for i in range(int(row)-1): #left wall
            cursorRowLeft = startingPoint_row+i
            MyUtilities.MoveCursor(cursorRowLeft, startingPoint_col)
            print ("|")

        for i in range(int(col)-1): #top wall
            cursorColTop = startingPoint_col+i
            MyUtilities.MoveCursor(startingPoint_row-1, cursorColTop)
            print ("_", end = "")
        print ()
        
        for i in range(int(row)-2): #right wall
            cursorRowRight = startingPoint_row+i
            cursorColRight = col+startingPoint_col
            MyUtilities.MoveCursor(cursorRowRight+1, cursorColRight-1)
            print ("|")

        for i in range(int(col)-1): #bottom wall 
            cursorColBot = startingPoint_col+i
            cursorRowBot = row+startingPoint_row
            MyUtilities.MoveCursor(cursorRowBot-1, cursorColBot)
            print ("_", end = "")
        print ()
        
    
        
    def PlayerWindow(self,user1): #player window used in dungeon, displays directions and more
        playerWindow = Hud()
        playerWindow.DrawHud("black", "white", 20, 60, 0, 61)
        MoveCursor(1,62)
        print ("W/A/S/D to move in the dungeon.")
        MoveCursor(2,62)
        print ("0 to go back to Town. ")
        MoveCursor(3, 62)
        print ("(V)iew player. ")
        MoveCursor(4, 62)
        print ("(I)tem activation. ") 

        MyUtilities.MoveCursor(8,62)        
        print (term.yellow(user1.name))
        MyUtilities.MoveCursor(9,62)
        print (term.yellow("Attack: "+str(user1.attack)))
        MyUtilities.MoveCursor(10,62)
        print (term.yellow("Defense: "+str(user1.defense)))
        MyUtilities.MoveCursor(11,62)
        print (term.yellow("Health: "+str(user1.health)))
        MoveCursor(12,62)
        print (term.yellow("Gold: " + str(user1.gold)))

        MoveCursor(17,62)
        print ("steps: "+str(user1.steps)) 
        MoveCursor(18,62)
        print ("Floor level:"+str(user1.floorLevel))
        
    def MarketWindows(self, user1): #function called in market to make all windows
        marketWindows = Hud()
        marketWindows.DrawHud("black", "white", 20, 60, 0, 61)
        marketWindows.DrawHud("black", "white", 15, 60, 21, 61) 
        marketWindows.DrawHud("Black", "White", 15, 60, 36, 61)
        marketWindows.DrawHud("black", "white", 8, 120, 51, 0)

    def EnemyWindow(self):
        enemyWindow = Hud()
        enemyWindow.DrawHud("black", "white", 15, 60, 21, 61)
        
    def ItemWindow(self):
        itemWindow = Hud()
        itemWindow.DrawHud("Black", "White", 15, 60, 36, 61)

    def SystemHud(self):
        systemMessage = Hud()
        systemMessage.DrawHud("black", "white", 8, 120, 51, 0) 

    def SystemMessage(self):
        cursorLocation = 52
        messageNum = 0
        while True:
            if (len(self.colorsList))>6:#making sure message screen does not pass 6
                    self.colorsList.pop(0)
            else:
                break
        
        #while True: #loop every input  
        while True:          
            if (len(self._message))>6:#making sure message screen does not pass 6
                self._message.pop(0)#gets rid of oldest message
            else:
                break
        for i in range (len(self._message)):  
                    
            MyUtilities.MoveCursor(cursorLocation, 4)#recurring move cursor to bottom left of screen, row changing every iteration of loop
            cursorLocation +=1
            print (" "*70,end = "")#overwrite old messages
        cursorLocation = 52
        for i in range(len(self._message)):#?
            MyUtilities.MoveCursor(cursorLocation, 4)
            cursorLocation +=1  #increment
            #for i in range(len(self.colorsList)): 
            fc = self.colorsList[i]
            bc = "black"
            color = getattr(term, fc+"_on_"+bc)
            print (color(self._message[i]), end = "", flush=True)#references incremented number to list, displaying next message     
            #print(color(self.symbol), end="", flush = True)           
        cursorLocation = 52                      
        messageNum +=1 #increment


    def OrchardHud(): #orchard HUD
        OrchardWindow = Hud()
        OrchardWindow.DrawHud("black", "white", 20, 60, 0, 61)
        MyUtilities.MoveCursor(2,62) 
        print ("W/A/S/D yo move in the orchard.")
        MyUtilities.MoveCursor(3,62)
        print("(P) to plant a new tree.")
        MyUtilities.MoveCursor(4,62)
        print("(I) to view type of tree. ")
        MyUtilities.MoveCursor(5,62)
        print("(T) to plant a new kind of tree.")
        MyUtilities.MoveCursor(6,62)
        print("0 to go back to the Town.")