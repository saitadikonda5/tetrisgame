import tkinter
from tkinter import *
import random
from time import sleep

#Make directions and gameover and automatic falling piece and restart game

class GameBoard():
  
    def __init__(self,master): 

        self.master = master
        self.master.title("Tetris")        

        self.canvas = Canvas(self.master, width = 40*(10), height = 40*(16))
        self.canvas.pack(side = RIGHT)

        
        start = Button(text = 'Start Game', command = self.startGame)
        start.config(height = 4,width = 15)
        start.pack(side = RIGHT, padx = 70)
        self.initUI()
        
        
    def initUI(self):   

        self.emptyColor = "grey"
        self.board = [[self.emptyColor]*10 for i in range(16)]   #Make gameboard
        self.width = 10 #number of columns
        self.height = 16  #number of rows
        
        for row in range(self.height):   #draw gameboard
            for col in range(self.width):
                self.drawCell(row,col)

        self.gameOver = False
        
        
    def drawCell(self,row,col,color = 'grey'):
        x1 = 40 * col
        y1 = 40 * row
        x2 = x1 + 40
        y2 = y1 + 40
        self.canvas.create_rectangle(x1,y1,x2,y2, fill = color)

    def drawPiece(self,x1=0,y1=3):  #draw a random piece
        colors = ['blue', 'red', 'purple', 'black', 'orange', 'pink', 'yellow']
        piece = pieces()
        pieceList = piece.getAllPieces()
        self.piece = pieceList[random.randint(0,6)]
        self.pieceColor = colors[pieceList.index(self.piece)]
        self.pieceRow = x1
        self.pieceCol = y1
        self.movePiece(0,3)
        

    def movePiece(self,x1,y1):
        self.pieceRow = x1
        self.pieceCol = y1
        rowOffset = 0
        for row in self.piece:
            colOffset = 0
            for col in row:
                if col == True: 
                    self.drawCell(x1+rowOffset,y1+colOffset,self.pieceColor)
                colOffset += 1
            rowOffset += 1

    def placePiece(self):  #put piece in its permanent location
        rowOffset = 0
        for row in self.piece:
            colOffset = 0
            for col in row:
                if col == True:
                    self.board[self.pieceRow+rowOffset][self.pieceCol+colOffset] = self.pieceColor
                colOffset += 1
            rowOffset += 1
        
    def startGame(self):
        # Cre
        self.reStart()
        self.drawPiece()

        self.move()



    def resetBoard(self,oldRow,oldCol):
        for row in range(len(self.piece)):
            for col in range(len(self.piece[0])):
                if self.board[oldRow+row][oldCol+col] == 'grey':
                    self.drawCell(oldRow+row,oldCol+col)

    def move(self):
        
        self.master.bind('<Down>',self.goDown)
        self.master.bind('<Left>',self.goLeft)
        self.master.bind('<Right>',self.goRight)
        self.master.bind('<Up>',self.rotate)
        


    def auto_fallPiece(self): #FINISH
    
        if self.collide(self.pieceRow+1,self.pieceCol) == False:
            self.resetBoard(self.pieceRow,self.pieceCol)
            self.movePiece(self.pieceRow+1,self.pieceCol)
        else:
            self.placePiece()
            self.drawPiece()
        
    
    def reStart(self):  
        self.canvas.delete(ALL)
        self.initUI()
        
       
            
    def goDown(self, event):
        if self.collide(self.pieceRow+1,self.pieceCol) == True and self.gameOver == True:       
            self.reStart()
        elif self.collide(self.pieceRow+1,self.pieceCol) == False:
            self.resetBoard(self.pieceRow,self.pieceCol)
            self.movePiece(self.pieceRow+1,self.pieceCol)
        else:
            self.placePiece()
            self.drawPiece()
            

       
    def goLeft(self,event):
        if self.collide(self.pieceRow,self.pieceCol-1) == True and self.gameOver == True:       
            self.reStart()
        elif self.collide(self.pieceRow,self.pieceCol-1) == False:
                self.resetBoard(self.pieceRow,self.pieceCol)
                self.movePiece(self.pieceRow,self.pieceCol-1)
        else:
            self.placePiece()
            self.drawPiece()

       
       

    def goRight(self, event):
        if self.collide(self.pieceRow,self.pieceCol+1) == True and self.gameOver == True:       
            self.reStart()
        elif self.collide(self.pieceRow,self.pieceCol+1) == False:  
                self.resetBoard(self.pieceRow,self.pieceCol)      #Reset board for the piece before it is moved
                self.movePiece(self.pieceRow,self.pieceCol+1)     #Move piece if it doesn't collide anywhere
        else:
            self.placePiece()   #if it does collide, then put piece in it's permanent location
            self.drawPiece()   #Make a new piece to start again
        
    def rotate(self,event):
        
        newPiece = []
        
        #Makes a new rotated piece by changing the list (self.piece)
        for col in range(len(self.piece[0])-1,-1,-1):
            newRow = []
            for row in range(len(self.piece)):
                newRow.append(self.piece[row][col])
            newPiece.append(newRow)

        self.resetBoard(self.pieceRow,self.pieceCol)
        self.piece = newPiece
        if self.collide(self.pieceRow,self.pieceCol) == True and self.gameOver == True:       
            self.reStart()
        elif (self.collide(self.pieceRow,self.pieceCol) == False):
            self.movePiece(self.pieceRow,self.pieceCol)
        else:
            self.placePiece()
            self.drawPiece()
        
    
         
    
    def collide(self,newRow,newCol):
        rowOffset = 0
        for row in self.piece:
            colOffset = 0
            for col in row:
                location = [newRow+rowOffset, newCol+colOffset]
                if col == True: # if cell isn't empty:
                    if (location[0] > 15): # if cell is too far to the right
                        return True
                    if (location[1] > 9): # if cell is too far down
                        return True
                    if (location[1] < 0): # if cell is too far to the left
                        return True
                    if self.board[location[0]][location[1]] != self.emptyColor: #if the cell is not empty
                        if (newRow == 1):
                            self.gameOver = True
                            return True
                        return True
                colOffset += 1
            rowOffset += 1
        return False  
        
    
        
class pieces():
            iPiece = [
                    [True,True,True,True]
            ]
            jPiece = [
                    [True,False,False],
                    [True,True,True]
            ]
            lPiece = [
                    [False,False,True],
                    [True,True,True]
            ]
            oPiece = [
                    [True,True],
                    [True,True]
            ]
            sPiece = [
                    [False,True,True],
                    [True,True,False]
            ]
            tPiece = [
                    [False,True,False],
                    [True,True,True]
            ]
            zPiece = [
                    [True,True,False],
                    [False,True,True]
            ]
            pieceList = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
            def getAllPieces(self):
                    return pieces.pieceList

def main():
    root = Tk()
    root.geometry("450x450")
    ex = GameBoard(root)
    root.mainloop()  


if __name__ == '__main__':
    main()