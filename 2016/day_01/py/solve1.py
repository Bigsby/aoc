#! /usr/bin/python3

from common import getInput, getNewHeading, headingSteps


def getNewPosition(currentPosition, heading, distance):
    step = headingSteps[heading]
    return currentPosition[0] + distance * step[0], currentPosition[1] + distance * step[1]


def main():
    instructions = list(getInput())
    currentPosition = (0,0)
    currentHeading = 0

    for direction, distance in instructions:
        currentHeading = getNewHeading(currentHeading, direction)
        currentPosition = getNewPosition(currentPosition, currentHeading, distance)

    result = abs(currentPosition[0]) + abs(currentPosition[1])
    print("Blocks away:", result)
        


if __name__ == "__main__":
    main()
