#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from collections import Counter
import re

Room = Tuple[str,int,str]


def isRoomValid(name: str, checksum: str) -> bool:
    name = name.replace("-", "")
    counts: Dict[str,int] = Counter(name)
    processedChecksum = "".join([ letter for letter, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:5] ])
    return processedChecksum == checksum


def part1(rooms: List[Room]) -> int:
    return sum([ id for name, id, checksum in rooms if isRoomValid(name, checksum)])


A_ORD = ord("a")
Z_ORD = ord("z")
DASH_ORD = ord("-")
SPACE_ORD = ord(" ")
def getNextChar(c: int) -> int:
    if c == DASH_ORD or c == SPACE_ORD:
        return SPACE_ORD
    if c == Z_ORD:
        return A_ORD
    else:
        return c + 1


def rotateName(name: str, count: int) -> str:
    nameInts = [ ord(c) for c in name ]
    for _ in range(count):
        for i in range(len(nameInts)):
            nameInts[i] = getNextChar(nameInts[i])
    return "".join([ chr(c) for c in nameInts ])


SEARCH_NAME = "northpole object storage"
def part2(rooms: List[Room]) -> int:
    for name, id, checksum in rooms:
        if isRoomValid(name, checksum) and rotateName(name, id) == SEARCH_NAME:
            return id
    raise Exception("Room not found")


lineRegex = re.compile(r"^(?P<name>[a-z\-]+)-(?P<id>\d+)\[(?P<checksum>\w+)\]$")
def parseLine(line: str) -> Room:
    match = lineRegex.match(line)
    if match:
        return match.group("name"), int(match.group("id")), match.group("checksum")
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Room]:
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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()