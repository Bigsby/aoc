#! /usr/bin/python3

from common import getInput, Grid, State


class DirectionalGrid(Grid):
    def __init__(self):
        self.occupiedTolerance = 4
        Grid.__init__(self)


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
    def getNeighbors(self, row, column):
        neighbors = []
        for rowStep, columnStep in DirectionalGrid.directionSteps:
            currentNeighbor = (row + rowStep, column + columnStep)
            while self.isNeighborValid(currentNeighbor) and self.rows[currentNeighbor[0]][currentNeighbor[1]] == State.FLOOR:
                currentNeighbor = (currentNeighbor[0] + rowStep, currentNeighbor[1] + columnStep)

            neighbors.append(currentNeighbor)
   
        return neighbors


def main():
    grid = DirectionalGrid()
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
