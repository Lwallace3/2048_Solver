import re
import math
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from py2048_classes import Tile, Board


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
        return maxVal(board, depth, player, move)
    elif player == 2:
        return expVal(board, depth, player, move)


def maxVal(board, depth, player, move):
    score = 0
    for i in board.possible_moves():
        x = board.export_state()
        tempBoard = Board(x)
        tempBoard.make_move(i)

        currentScore = expectimax(tempBoard, depth - 1, 2, i)
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
        currentScore = expectimax(tempBoard, depth - 1, 1, move)
        totalScore += (0.2 * currentScore[0])

        tempBoard = Board(x)
        twoTile = Tile(1)
        tempBoard.grid[i[1]][i[0]] = twoTile
        currentScore = expectimax(tempBoard, depth - 1, 1, move)
        totalScore += (0.8 * currentScore[0])

    average = totalScore / len(emptyCells)
    return average, move


def utilityScore(board):
    utility = 0
    leftVal = 0
    rightVal = 0
    bottomLeftVal = 0
    bottomRightVal = 0
    boardGrid = board.export_state()

    comparisonGridLeft = [
        [2 ** 6, 2 ** 5, 2 ** 4, 2 ** 3],
        [2 ** 5, 2 ** 4, 2 ** 3, 2 ** 2],
        [2 ** 4, 2 ** 3, 2 ** 2, 2 ** 1],
        [2 ** 3, 2 ** 2, 2 ** 1, 2 ** 1]
    ]
    comparisonGridRight = [
        [2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6],
        [2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5],
        [2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4],
        [2 ** 1, 2 ** 1, 2 ** 2, 2 ** 3]
    ]
    comparisonGridBottomRight = [
        [2 ** 1, 2 ** 1, 2 ** 2, 2 ** 3],
        [2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4],
        [2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5],
        [2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6]
    ]
    comparisonGridBottomLeft = [
        [2 ** 3, 2 ** 2, 2 ** 1, 2 ** 1],
        [2 ** 4, 2 ** 3, 2 ** 2, 2 ** 1],
        [2 ** 5, 2 ** 4, 2 ** 3, 2 ** 2],
        [2 ** 6, 2 ** 5, 2 ** 4, 2 ** 3]
    ]

    for x in range(0, 4):
        for y in range(0, 4):
            if boardGrid[x][y] != None:
                val = board.grid[x][y].get_tile_value()
                leftVal += val * comparisonGridLeft[x][y]
                rightVal += val * comparisonGridRight[x][y]
                bottomRightVal += val * comparisonGridBottomRight[x][y]
                bottomLeftVal += val * comparisonGridBottomLeft[x][y]

    utility = max(rightVal, max(leftVal, max(bottomLeftVal, bottomRightVal)))
    return utility


def update_grid(driver):
    grid = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]

    tc = driver.find_element_by_class_name('tile-container')
    tile_html = tc.get_attribute('innerHTML')
    find_values = re.findall(r'tile-\b\d{1,8}\b', tile_html)
    find_positions = re.findall(r'tile-position-\d-\d', tile_html)

    for x in range(len(find_values)):
        x_coord = int(find_positions[x][-3]) - 1
        y_coord = int(find_positions[x][-1]) - 1
        real_value_of_tile = int(find_values[x].replace('tile-', ''))
        log_value_of_tile = math.log(real_value_of_tile, 2)
        grid[y_coord][x_coord] = Tile(log_value_of_tile)
    return grid


def main():
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/chromedriver.exe')
    driver.get('https://play2048.co/')
    body = driver.find_element_by_tag_name('body')
    board = Board()
    key_map = {
        'UP': Keys.ARROW_UP,
        'RIGHT': Keys.ARROW_RIGHT,
        'DOWN': Keys.ARROW_DOWN,
        'LEFT': Keys.ARROW_LEFT
    }
    board.grid = update_grid(driver=driver)

    while True:
        begin = time.time()
        move = pickMove(board)
        next_key = key_map[move]
        body.send_keys(next_key)

        print(move, " at a time of ", (time.time() - begin))
        board.grid = update_grid(driver=driver)


if __name__ == "__main__":
    main()
