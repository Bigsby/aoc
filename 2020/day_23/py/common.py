import sys, os


debug = False
singleLineDebug = True

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for c in file.read().strip():
            yield int(c)


def getDestinationCupIndex(current, others):
    under = current - 1
    while under:
        if under in  others:
            return others.index(under)
        under -= 1
    return others.index(max(others))


def playGame(cups, moves):
    global debug
    move = 0

    while move < moves:
        move += 1
        currentCup = cups[0]
        selectedCups = cups[1:4]
        otherCups = cups[4:]
        destinationIndex = getDestinationCupIndex(currentCup, otherCups)
        if debug:
            print("-- move", move, "--")
            print("cups:", "".join(["(", str(currentCup), ")"]), " ".join(map(str, selectedCups)), " ".join(map(str, otherCups)))
            print("pick up:", ", ".join(map(str, selectedCups)))
            print("destination:", otherCups[destinationIndex])
            print()
        if singleLineDebug and move % 1000 == 0:
            print("Move:", move, "\tCurrent:", currentCup, "\r", end="")
        cups = otherCups[:destinationIndex + 1]
        cups += selectedCups
        cups += otherCups[destinationIndex + 1:]
        cups.append(currentCup)
    print()

    return cups

