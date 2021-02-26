#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from enum import Enum


PROPS = [ "children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes" ]
NA_PROP = -1


def buildPropDict() -> Dict[str,int]:
    return { prop: NA_PROP for prop in PROPS }
    

class AuntRecord():
    def __init__(self, number: str, prop1Name: str, prop1Value: str, prop2Name: str, prop2Value: str, prop3Name: str, prop3Value: str):
        self.number = int(number)
        self.props = buildPropDict()
        self.setProp(prop1Name, prop1Value)
        self.setProp(prop2Name, prop2Value)
        self.setProp(prop3Name, prop3Value)

    def setProp(self, name:str, value:str):
        self.props[name] = int(value)


class Operator(Enum):
    EQUAL = 0,
    GREATER = 1,
    LESS = 2


class Reading():
    def __init__(self, value: int, operator: Operator = Operator.EQUAL):
        self.value = value
        self.operator = operator


MFCSAN_READING: Dict[str,Reading] = {
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
def isValidRecord(record: AuntRecord, checkOperator: bool = False) -> bool:
    for prop in MFCSAN_READING:
        recordValue = record.props[prop]
        if recordValue == NA_PROP:
            continue
        reading = MFCSAN_READING[prop]
        readingValue = reading.value
        if checkOperator:
            if reading.operator == Operator.EQUAL and recordValue != readingValue \
                or reading.operator == Operator.GREATER and recordValue <= readingValue \
                or reading.operator == Operator.LESS and recordValue >= readingValue:
                return False
        elif recordValue != readingValue:
            return False
    return True


def solve(aunts: List[AuntRecord]) -> Tuple[int,int]:
    return (
        next(filter(lambda record: isValidRecord(record), aunts)).number, 
        next(filter(lambda record: isValidRecord(record, True), aunts)).number
    )


lineRegex = re.compile(r"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$")
def parseLine(line: str):
    match = lineRegex.match(line)
    if match:
        return AuntRecord(*match.group(1, 2, 3, 4, 5, 6, 7))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[AuntRecord]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()