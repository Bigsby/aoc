#! /usr/bin/python3

from common import getInput, Grid

class AdjacentGrid(Grid):
    def __init__(self):
        self.occupiedTolerance = 3
        Grid.__init__(self)


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


def main():
    grid = AdjacentGrid()
    getInput(grid)
    updatedCount = 1
    iterations = 0
    while updatedCount != 0:
        iterations += 1
        updatedCount = grid.goToNextState()

    print("Iterations:", iterations)
    print("Occupied count:", grid.getOccupiedCount())


if __name__ == "__main__":
    main()
