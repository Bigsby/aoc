import sys, os
from functools import reduce


class Grid():
    def __init__(self):
        self.lights = []

    def addLine(self, line):
        newLine = []
        for c in line:
            newLine.append(1 if c == "#" else 0)
        self.lights.append(newLine)

    def __str__(self):        
        return str(self.lights)


    def print(self):
        length = len(self.lights)
        for row in range(length):
            print(row, self.lights[row])

        
    def getNeighbors(self, row, column):
        return [ 
            (row - 1, column -1),
            (row - 1, column),
            (row - 1, column + 1),
            (row, column - 1),
            (row, column + 1),
            (row + 1, column -1),
            (row + 1, column),
            (row + 1, column +1)
        ]

    def isNeighborValid(self, coordinate):
        limit = len(self.lights)
        return coordinate[0] >= 0 and coordinate[0] < limit and coordinate[1] >= 0 and coordinate[1] < limit


    def getNeighborsOnCount(self, row, column):
        count = 0
        neighbors = self.getNeighbors(row, column)
        for neighbor in neighbors:
            if self.isNeighborValid(neighbor):
                count += self.lights[neighbor[0]][neighbor[1]]
        return count


    def calculateNextStep(self):
        length = len(self.lights)
        newState = [ [0] * length for i in range(length) ]
        for row in range(length):
            for column in range(length):
                neighbors = self.getNeighborsOnCount(row, column)
                if self.lights[row][column]:
                    newState[row][column] = 1 if neighbors == 2 or neighbors == 3 else 0
                else:
                    newState[row][column] = 1 if neighbors == 3 else 0
        self.lights = newState

    def lightsOnCount(self):
        return reduce(lambda rowCount, row: rowCount + reduce(lambda columnCount, column: columnCount + column, row, 0), self.lights, 0)


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        grid = Grid()
        for line in file.readlines():
            grid.addLine(line.strip())
        return grid
