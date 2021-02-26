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


def solve(connections: Dict[int,List[int]]) -> Tuple[int,int]:
    part1Result = len(getProgramGroup(0, connections))
    groupsCount = 0
    while connections:
        groupsCount += 1
        for connection in getProgramGroup(next(iter(connections.keys())), connections):
            if connection in connections:
                del connections[connection]    
    return part1Result, groupsCount


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()