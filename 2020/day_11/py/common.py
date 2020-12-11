import sys, os
from enum import Enum
from functools import reduce


class State(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


class Grid():
    def __init__(self):
        self.rows = []


    def addRow(self, row):
        newRow = []
        for c in row:
            newRow.append(State(c))
        self.rows.append(newRow)


    def print(self):
        for row in self.rows:
            print("".join(map(lambda s: s.value, row)))

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
        rowLimit = len(self.rows)
        columnLimit = len(self.rows[0])
        return coordinate[0] >= 0 and coordinate[0] < rowLimit and coordinate[1] >= 0 and coordinate[1] < columnLimit


    def getOccupiedNeighborsCount(self, row, column):
        count = 0
        neighbors = self.getNeighbors(row, column)
        for neighbor in neighbors:
            if self.isNeighborValid(neighbor) and self.rows[neighbor[0]][neighbor[1]] == State.OCCUPIED:
                count += 1
        return count


    def getNewState(self, row, column):
        currentState = self.rows[row][column]
        if currentState == State.FLOOR:
            return False, State.FLOOR
        occupiedCount = self.getOccupiedNeighborsCount(row, column)
        if currentState == State.EMPTY and occupiedCount == 0:
            return True, State.OCCUPIED
        if currentState == State.OCCUPIED and occupiedCount > 3:
            return True, State.EMPTY
        return False, currentState


    def goToNextState(self):
        rowCount = len(self.rows)
        columnCount = len(self.rows[0])
        newGrid = [ [State.FLOOR] * columnCount for i in range(rowCount) ]
        seatsChangedCount = 0
        for row in range(rowCount):
            for column in range(columnCount):
                changed, newState = self.getNewState(row, column)
                seatsChangedCount += changed
                newGrid[row][column] = newState
        self.rows = newGrid
        return seatsChangedCount
        

    def getOccupiedCount(self):
        return reduce(lambda rowCount, row: rowCount + reduce(lambda columnCount, column: columnCount + (column == State.OCCUPIED), row, 0), self.rows, 0)


        

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
            grid.addRow(line.strip())
        return grid
