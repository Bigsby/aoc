#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple

Scanners = Dict[int,int]


def runPacket(scanners: Scanners, offset: int) -> int:
    positions: Dict[int,int] = { layer: 0 for layer in scanners.keys() }
    currentLayer: int = 0
    severity: int = 0
    while currentLayer < max(scanners.keys()) + 1:
        if currentLayer in positions and (currentLayer + offset) % (scanners[currentLayer] * 2 - 2) == 0:
            severity += currentLayer * scanners[currentLayer]
        currentLayer += 1
    return severity


def part1(scanners: Scanners) -> int:
    return runPacket(scanners, 0)


def part2(scanners: Scanners):
    offset = 1
    firstScannerCycle = scanners[0] * 2 - 2

    while offset % firstScannerCycle == 0 or runPacket(scanners, offset):
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