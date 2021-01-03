#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


def isRoomValid(name, checksum):
    name = name.replace("-", "")
    counts = {}
    for letter in name:
        counts[letter] = name.count(letter)
    processedChecksum = "".join([ letter for letter, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:5] ])
    return processedChecksum == checksum


def part1(rooms):
    return sum([ id for name, id, checksum in rooms if isRoomValid(name, checksum)])


A_ORD = ord("a")
Z_ORD = ord("z")
DASH_ORD = ord("-")
SPACE_ORD = ord(" ")
def getNextChar(c):
    if c == DASH_ORD or c == SPACE_ORD:
        return SPACE_ORD
    if c == Z_ORD:
        return A_ORD
    else:
        return c + 1


def rotateName(name, count):
    name = [ ord(c) for c in name ]
    for _ in range(count):
        for i in range(len(name)):
            name[i] = getNextChar(name[i])
    return "".join([ chr(c) for c in name ])


SEARCH_NAME = "northpole object storage"
def part2(rooms):
    for name, id, checksum in rooms:
        if isRoomValid(name, checksum) and rotateName(name, id) == SEARCH_NAME:
            return id


lineRegex = re.compile(r"^(?P<name>[a-z\-]+)-(?P<id>\d+)\[(?P<checksum>\w+)\]$")
def parseLine(line):
    match = lineRegex.match(line)
    return match.group("name"), int(match.group("id")), match.group("checksum")


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