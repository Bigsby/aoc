#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple

Scanners = Dict[int,int]


def getCycles(scanners: Scanners) -> Dict[int,int]:
    return { layer: 2 * (range - 1) for layer, range in scanners.items() }


def part1(scanners: Scanners) -> int:
    cycles = getCycles(scanners)
    severity: int = 0
    for currentLayer in range(max(scanners.keys()) + 1):
        if currentLayer in cycles and currentLayer % cycles[currentLayer] == 0:
            severity += currentLayer * scanners[currentLayer]
        currentLayer += 1
    return severity


def runPacketUntilCaught(cycles: Scanners, offset: int) -> int:
    for currentLayer in range(max(cycles.keys()) + 1):
        if currentLayer in cycles and (currentLayer + offset) % cycles[currentLayer] == 0:
            return False
        currentLayer += 1
    return True


def part2(scanners: Scanners):
    cycles = getCycles(scanners)
    offset = 1
    while not runPacketUntilCaught(cycles, offset):
        offset += 1
    return offset


def parseLine(line: str) -> Tuple[int,int]:
    depth, range = line.split(":")
    return int(depth.strip()), int(range.strip())


def getInput(filePath: str) -> Dict[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { scanner: depth  for scanner, depth in map(parseLine, file.readlines()) }


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