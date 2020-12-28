#! /usr/bin/python3

import sys, os, time
import re

def getNewHeading(currentHeading, direction):
    newHeading = currentHeading + (90 if direction == "R" else -90)
    if newHeading < 0:
        return 360 + newHeading
    if newHeading > 270:
        return newHeading - 360
    return newHeading


headingSteps = {
    0: (0,1),       # facing North
    90: (1,0),      # facing East
    180: (0,-1),    # facing South
    270: (-1,0)     # facing West
}


def getNewPosition(currentPosition, heading, distance):
    step = headingSteps[heading]
    return currentPosition[0] + distance * step[0], currentPosition[1] + distance * step[1]


def getDistanceToOrigin(position):
    return abs(position[0]) + abs(position[1])


def part1(puzzleInput):
    currentPosition = (0,0)
    currentHeading = 0

    for direction, distance in puzzleInput:
        currentHeading = getNewHeading(currentHeading, direction)
        currentPosition = getNewPosition(currentPosition, currentHeading, distance)

    return getDistanceToOrigin(currentPosition)


def getVisitedPositions(position, heading, distance):
    step = headingSteps[heading]
    for i in range(1, distance + 1):
        yield position[0] - (i * step[0]), position[1] - (i * step[1])


def part2(puzzleInput):
    currentPosition = (0,0)
    currentHeading = 0
    visitedPositions = [ currentPosition ]
    done = False

    for direction, distance in puzzleInput:
        currentHeading = getNewHeading(currentHeading, direction)
        newPositions = getVisitedPositions(currentPosition, currentHeading, distance)
        for newPosition in newPositions:
            currentPosition = newPosition
            if currentPosition in visitedPositions:
                done = True
                break
            else:
                visitedPositions.append(currentPosition)
        if done:
            break

    return getDistanceToOrigin(currentPosition)


instructionRegex = re.compile("^(?P<direction>[RL])(?P<distance>\d+),?\s?$")
def parseInstruction(instructionText):
    match = instructionRegex.match(instructionText)
    return (match.group("direction"), int(match.group("distance")))

def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseInstruction(instruction) for instruction in file.read().split(" ") ]


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