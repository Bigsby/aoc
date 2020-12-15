import sys, os
from typing import NamedTuple


def getNthTurn(turns: int) -> int:
    numbers = list(getInput())
    turn = 0
    occurrences = {}
    for number in numbers:
        turn += 1
        occurrences[number] = (turn, 0)

    lastNumber = numbers[-1]
    
    while turn < turns:
        turn += 1
        occurrence = occurrences[lastNumber]

        if occurrence[1] == 0:
            lastNumber = 0
        else:
            lastNumber = occurrence[0] - occurrence[1]

        if lastNumber in occurrences:
            lastNumberOccurrences = occurrences[lastNumber]
            occurrences[lastNumber] = (turn, lastNumberOccurrences[0])
        else:
            occurrences[lastNumber] = (turn, 0)

    return lastNumber
    

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        return list(map(lambda i: int(i), file.read().split(",")))
