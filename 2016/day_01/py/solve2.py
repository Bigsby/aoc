#! /usr/bin/python3

from common import getInput, getNewHeading, headingSteps


def getVisitedPositions(position, heading, distance):
    step = headingSteps[heading]
    for i in range(1, distance + 1):
        yield position[0] - (i * step[0]), position[1] - (i * step[1])
    

def main():
    instructions = list(getInput())
    currentPosition = (0,0)
    currentHeading = 0
    visitedPositions = [ currentPosition ]
    done = False

    for direction, distance in instructions:
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

    result = abs(currentPosition[0]) + abs(currentPosition[1])
    print("Blocks away:", result)


if __name__ == "__main__":
    main()
