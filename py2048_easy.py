"""
Python 2048 Game : Basic Console Based User Interface For Game Play

Originally written by Phil Rodgers, University of Strathclyde
"""

from py2048_classes import Board, Tile

import time
import math
import random

def pickMove(board):
    move = None
    topScore = 0
    for i in board.possible_moves():
        x = board.export_state()
        temp = Board(x)
        temp.make_move(i)

        x = expectimax(temp, 4, 2, i)

        if x[0] > topScore:
            topScore = x[0]
            move = x[1] 
    return move
            

def expectimax(board, depth, player, move):
    if depth == 0:
        return utilityScore(board), move
    elif player == 1:
        return maxVal(board,depth,player,move)
    elif player == 2:
        return expVal(board, depth,player,move)
    
def maxVal(board,depth,player,move):
    score = 0
    for i in board.possible_moves():
        x = board.export_state()
        tempBoard = Board(x)
        tempBoard.make_move(i)

        currentScore = expectimax(tempBoard, depth-1, 2, i)
        if currentScore[0] > score:
            score = currentScore[0]
            move = currentScore[1]

    return score, move
        
def expVal(board, depth, player, move):
    totalScore = 0
    emptyCells = board.empty()

    for i in emptyCells:
        x = board.export_state()
        tempBoard = Board(x)
        fourTile = Tile(2)
        tempBoard.grid[i[1]][i[0]] = fourTile
        currentScore = expectimax(tempBoard, depth-1, 1, move)
        totalScore += (0.2 * currentScore[0])

        tempBoard = Board(x)
        twoTile = Tile(1)
        tempBoard.grid[i[1]][i[0]] = twoTile
        currentScore = expectimax(tempBoard, depth-1, 1, move)
        totalScore += (0.8 * currentScore[0])
            
    average = totalScore/len(emptyCells)
    return average, move

def utilityScore(board):
    utility = 0
    leftVal = 0
    rightVal = 0
    bottomLeftVal = 0
    bottomRightVal = 0
    boardGrid = board.export_state()
    
    
    comparisonGridLeft = [
                [2**6, 2**5, 2**4, 2**3],
                [2**5, 2**4, 2**3, 2**2],
                [2**4, 2**3, 2**2, 2**1],
                [2**3, 2**2, 2**1, 2**1]
            ]
    comparisonGridRight = [
                [2**3, 2**4, 2**5, 2**6],
                [2**2, 2**3, 2**4, 2**5],
                [2**1, 2**2, 2**3, 2**4],
                [2**1, 2**1, 2**2, 2**3]
            ]
    comparisonGridBottomRight = [
                [2**1, 2**1, 2**2, 2**3],
                [2**1, 2**2, 2**3, 2**4],
                [2**2, 2**3, 2**4, 2**5],
                [2**3, 2**4, 2**5, 2**6]
            ]
    comparisonGridBottomLeft = [
                [2**3, 2**2, 2**1, 2**1],
                [2**4, 2**3, 2**2, 2**1],
                [2**5, 2**4, 2**3, 2**2],
                [2**6, 2**5, 2**4, 2**3]
            ]
    
    for x in range(0,4):
        for y in range(0,4):
            if boardGrid[x][y] != None:
                val = board.grid[x][y].get_tile_value() 
                leftVal += val * comparisonGridLeft[x][y]
                rightVal += val * comparisonGridRight[x][y]
                bottomRightVal += val * comparisonGridBottomRight[x][y]
                bottomLeftVal += val * comparisonGridBottomLeft[x][y]
           
    utility = max(rightVal, max(leftVal, max(bottomLeftVal, bottomRightVal)))
    return utility

    
def main():
#    allmoves = ['UP','LEFT','DOWN','RIGHT']
    board = Board()
    board.add_random_tiles(2)
    print("main code")

    move_counter = 0
    move = None
    move_result = False

    
    overalltime=time.time()
    while True:
        print("Number of successful moves:{}, Last move attempted:{}:, Move status:{}".format(move_counter, move, move_result))
        print(board)
       # print(board.print_metrics())
        if board.possible_moves()==[]:
            if (board.get_max_tile()[0]<2048):
                print("You lost!")
            else:
                print("Congratulations - you won!")
            break
        begin = time.time()
###################################### Your code should be inserted below 
###################################### (feel free to define additional functions to determine the next move)
   
        move = pickMove(board)
        print(move)
        board.make_move(move)

######################################  Do not   4 lines below      
######################################
        print("Move time: ", time.time()-begin)
        board.add_random_tiles(1)
        move_counter = move_counter + 1
    print("Average time per move:", (time.time()-overalltime)/move_counter)
    

if __name__ == "__main__":
    main()
    
    
def monteCarlo(board):
    maxGame = board.random_rollout(100)
    i = 0
    for i in range(100):
        boardCopy = board
        
        runGame = boardCopy.random_rolloutB(100)
        if(runGame[0] > maxGame[0]):
            maxGame = runGame
    return maxGame[1]


