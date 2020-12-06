#! /usr/bin/python3

from functools import reduce

from common import getInput


def updateMatrix(matrix, action, xstart, ystart, xend, yend):
    actionFun = lambda value: 0
    if action == "turn on":
        actionFun = lambda value: 1
    elif action == "toggle":
        actionFun = lambda value: 0 if value else 1

    for x in range(xstart, xend + 1):
        for y in range(ystart, yend + 1):
            matrix[x][y] = actionFun(matrix[x][y])


def getTurnedOn(matrix):
    return reduce(lambda rowCount, row: rowCount + reduce(lambda columnCount, column: columnCount + column, row), matrix, 0)


def main():
    matrix = [ [0] * 1000 for i in range(1000) ]
    for instruction in getInput():
        action, xstart, ystart, xend, yend = instruction
        updateMatrix(matrix, action, xstart, ystart, xend, yend) 

    print("Turned on count:", getTurnedOn(matrix))

if __name__ == "__main__":
    main()
