#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple

Scanners = Dict[int,int]


def part1(scanners: Scanners, cycles: Scanners) -> int:
    severity: int = 0
    for currentLayer in range(max(scanners.keys()) + 1):
        if currentLayer in cycles and currentLayer % cycles[currentLayer] == 0:
            severity += currentLayer * scanners[currentLayer]
    return severity


def runPacketUntilCaught(cycles: Scanners, offset: int) -> bool:
    for currentLayer in range(max(cycles.keys()) + 1):
        if currentLayer in cycles and (currentLayer + offset) % cycles[currentLayer] == 0:
            return False
    return True


def part2(cycles: Scanners):
    offset = 1
    while not runPacketUntilCaught(cycles, offset):
        offset += 1
    return offset


def solve(scanners: Scanners) -> Tuple[int,int]:
    cycles = { layer: 2 * (range - 1) for layer, range in scanners.items() }
    return (
        part1(scanners, cycles),
        part2(cycles)
    )


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()