#! /usr/bin/python3

import sys, os, time
from enum import Enum
from functools import reduce


class State(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


class Grid():
    def __init__(self):
        self.rows = []
        self.occupiedTolerance = 0
        self.getNeighbors = lambda _: []

    def addRow(self, row):
        newRow = []
        for c in row:
            newRow.append(State(c))
        self.rows.append(newRow)
    
    def _setOccupiedTolerance(self, tolerance):
        self.occupiedTolerance = tolerance
    
    def _setGetNeighbors(self, func):
        self.getNeighbors = func

    def clone(self, tolerance, getNeighborsFunc):
        clone = Grid()
        clone._setOccupiedTolerance(tolerance)
        clone._setGetNeighbors(getNeighborsFunc)
        for row in self.rows:
            clone.rows.append(list(row))
        return clone

    def print(self):
        for row in self.rows:
            print("".join(map(lambda s: s.value, row)))

    def isNeighborValid(self, coordinate):
        rowLimit = len(self.rows)
        columnLimit = len(self.rows[0])
        return coordinate[0] >= 0 and coordinate[0] < rowLimit and coordinate[1] >= 0 and coordinate[1] < columnLimit
 
    def getOccupiedNeighborsCount(self, row, column):
        count = 0
        neighbors = self.getNeighbors(self, row, column)
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
        if currentState == State.OCCUPIED and occupiedCount > self.occupiedTolerance:
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


def runGrid(grid):
    while grid.goToNextState():
        pass
    return grid.getOccupiedCount()


def getNeighbors1(_, row, column):
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


def part1(puzzleInput):
    return runGrid(puzzleInput.clone(3, getNeighbors1))


directionSteps = [ 
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]
def getNeighbors2(grid, row, column):
    neighbors = []
    for rowStep, columnStep in directionSteps:
        currentNeighbor = (row + rowStep, column + columnStep)
        while grid.isNeighborValid(currentNeighbor) and grid.rows[currentNeighbor[0]][currentNeighbor[1]] == State.FLOOR:
            currentNeighbor = (currentNeighbor[0] + rowStep, currentNeighbor[1] + columnStep)

        neighbors.append(currentNeighbor)

    return neighbors


def part2(puzzleInput):
    return runGrid(puzzleInput.clone(4, getNeighbors2))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    grid = Grid()
    with open(filePath, "r") as file:
        for line in file.readlines():
            grid.addRow(line.strip())
    return grid


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()