import sys, os, re

instructionRegex = re.compile("^(?P<direction>[RL])(?P<distance>\d+),?\s?$")


def getNewHeading(currentHeading, direction):
    newHeading = currentHeading + (90 if direction == "R" else -90)
    if newHeading < 0:
        return 360 + newHeading
    if newHeading > 270:
        return newHeading - 360
    return newHeading


headingSteps = {
    0: (0,1),
    90: (1,0),
    180: (0,-1),
    270: (-1,0)
}


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        contents = file.read()
        for instruction in contents.split(" "):
            match = instructionRegex.match(instruction)
            if match:
                yield (match.group("direction"), int(match.group("distance")))
            else:
                print("Didn't match:", instruction)
            
