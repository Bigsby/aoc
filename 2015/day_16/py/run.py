#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum



props = [ "children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes" ]
NA_PROP = "N/A"

def buildPropDict():
    return { prop: NA_PROP for prop in props }
    

class AuntRecord():
    def __init__(self, number, prop1Name, prop1Value, prop2Name, prop2Value, prop3Name, prop3Value):
        self.number = int(number)
        self.props = buildPropDict()
        self.setProp(prop1Name, prop1Value)
        self.setProp(prop2Name, prop2Value)
        self.setProp(prop3Name, prop3Value)

    def setProp(self, name, value):
        self.props[name] = int(value)

    def __str__(self):
        return f"{self.number} => {self.props}"
    def __repr__(self):
        return self.__str__()


class Operator(Enum):
    EQUAL = 0,
    GREATER = 1,
    LESS = 2


class Reading():
    def __init__(self, value, operator = Operator.EQUAL):
        self.value = value
        self.operator = operator


mfcsamReading = {
    "children": Reading(3),
    "cats": Reading(7, Operator.GREATER),
    "samoyeds": Reading(2),
    "pomeranians": Reading(3, Operator.LESS),
    "akitas": Reading(0),
    "vizslas": Reading(0),
    "goldfish": Reading(5, Operator.LESS),
    "trees": Reading(5, Operator.GREATER),
    "cars": Reading(2),
    "perfumes": Reading(1)
}
def isValidRecord(record, checkOperator = False):
    for prop in mfcsamReading:
        recordValue = record.props[prop]
        if recordValue == NA_PROP:
            continue
        reading = mfcsamReading[prop]
        readingValue = reading.value
        if checkOperator:
            if reading.operator == Operator.EQUAL and recordValue != readingValue:
                return False
            if reading.operator == Operator.GREATER and recordValue <= readingValue:
                return False
            if reading.operator == Operator.LESS and recordValue >= readingValue:
                return False
        elif recordValue != readingValue:
            return False
    return True


def getAuntNumber(aunts, checkOperator = False):
    for record in aunts:
        if isValidRecord(record, checkOperator):
            return record.number


def part1(puzzleInput):
    return getAuntNumber(puzzleInput)


def part2(puzzleInput):
    return getAuntNumber(puzzleInput, True)


lineRegex = re.compile(r"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$")
def parseLine(line):
    return AuntRecord(*lineRegex.match(line).group(1, 2, 3, 4, 5, 6, 7))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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