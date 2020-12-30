#! /usr/bin/python3

import sys, os, time


def getNeighbors(row, column):
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

class Grid():
    def __init__(self, lights = []):
        self.lights = lights

    def addLine(self, line):
        newLine = []
        for c in line:
            newLine.append(1 if c == "#" else 0)
        self.lights.append(newLine)
    
    @staticmethod
    def _fromLights(lights):
        return Grid(lights)

    def __str__(self):        
        return str(self.lights)

    def print(self):
        length = len(self.lights)
        for row in range(length):
            print(row, self.lights[row])

    def isNeighborValid(self, coordinate):
        limit = len(self.lights)
        return coordinate[0] >= 0 and coordinate[0] < limit and coordinate[1] >= 0 and coordinate[1] < limit

    def getNeighborsOnCount(self, row, column):
        count = 0
        neighbors = getNeighbors(row, column)
        for neighbor in neighbors:
            if self.isNeighborValid(neighbor):
                count += self.lights[neighbor[0]][neighbor[1]]
        return count

    def calculateNextStep(self, alwaysOn = []):
        for coordinate in alwaysOn:
            self.lights[coordinate[0]][coordinate[1]] = 1
            
        length = len(self.lights)
        newState = [ [0] * length for i in range(length) ]
        for row in range(length):
            for column in range(length):
                neighbors = self.getNeighborsOnCount(row, column)
                if self.lights[row][column]:
                    newState[row][column] = 1 if neighbors == 2 or neighbors == 3 else 0
                else:
                    newState[row][column] = 1 if neighbors == 3 else 0
        for coordinate in alwaysOn:
            newState[coordinate[0]][coordinate[1]] = 1
        return Grid._fromLights(newState)
        
    def lightsOnCount(self):
        return sum([ sum([ column for column in row]) for row in self.lights ])


def runSteps(grid, alwaysOn = []):
    for _ in range(100):
        grid = grid.calculateNextStep(alwaysOn)
    return grid.lightsOnCount()


def part1(puzzleInput):
    return runSteps(puzzleInput)


def part2(puzzleInput):
    limit = len(puzzleInput.lights) - 1
    alwaysOn = [
        (0, 0),
        (0, limit),
        (limit, 0),
        (limit, limit)
    ]
    return runSteps(puzzleInput, alwaysOn)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = Grid()
        for line in file.readlines():
            grid.addLine(line.strip())
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