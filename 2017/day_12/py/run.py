#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Set, Tuple
import re


def getProgramGroup(program: int, connections: Dict[int,List[int]], soFar: Set[int] = set()) -> Set[int]:
    soFar.add(program)
    for connection in connections[program]:
        if connection not in soFar:
            soFar |= getProgramGroup(connection, connections)
    return soFar


def part1(connections: Dict[int,List[int]]) -> int:
    return len(getProgramGroup(0, connections))


def part2(connections: Dict[int,List[int]]) -> int:
    groupsCount = 0
    while connections:
        groupsCount += 1
        for connection in getProgramGroup(next(iter(connections.keys())), connections):
            if connection in connections:
                del connections[connection]    
    return groupsCount


lineRegex = re.compile(r"^(?P<one>\d+)\s<->\s(?P<two>.*)$")
def parseLine(line: str) -> Tuple[int,List[int]]:
    match = lineRegex.match(line)
    if match:
        return int(match.group("one")), list(map(int, match.group("two").split(",")))
    raise Exception("Bad format", line)

def getInput(filePath: str) -> Dict[int,List[int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { program: connections for program, connections in[ parseLine(line) for line in file.readlines() ] }


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