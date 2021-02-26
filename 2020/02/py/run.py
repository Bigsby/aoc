#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple
import re

Line = Tuple[int,int,str,str]


def countValid(lines: List[Line], validationFunc: Callable[[Line],bool]) -> int:
    return len(list(filter(validationFunc, lines)))


def isLineValid(line: Line) -> bool:
    minimum, maximum, letter, password = line
    occurenceCount = password.count(letter) 
    return occurenceCount >= minimum and occurenceCount <= maximum


def isLineValid2(line: Line) -> bool:
    first, second, letter, password = line 
    return (password[first - 1] == letter) ^ (password[second - 1] == letter)


def solve(lines: List[Line]) -> Tuple[int,int]:
    return (
        countValid(lines, isLineValid),
        countValid(lines, isLineValid2)
    )


lineRegex = re.compile(r"^(\d+)-(\d+)\s([a-z]):\s(.*)$")
def parseLine(line: str) -> Line:
    match = lineRegex.match(line)
    if match:
        min, max, letter, password = match.group(1, 2, 3, 4)
        return (int(min), int(max), letter, password)
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Line]:
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