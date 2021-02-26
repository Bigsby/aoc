#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple
import re
from itertools import product
from heapq import heappop, heappush

Coordinate = complex
GEOLOGIC_X_CONSTANT = 16807
GEOLOGIC_Y_CONSTANT = 48271
EROSION_CONSTANT = 20183


def getGeologicIndex(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate,int]) -> int:
    if coordinate == 0 or coordinate == target:
        return 0
    x, y = int(coordinate.real), int(coordinate.imag)
    if x == 0:
        return y * GEOLOGIC_Y_CONSTANT
    elif y == 0:
        return x * GEOLOGIC_X_CONSTANT
    return getErosionLevel(x - 1 + y * 1j, depth, target, calculated) \
        * getErosionLevel(x + (y - 1)* 1j, depth, target, calculated)


def getErosionLevel(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate,int]) -> int:
    if coordinate not in calculated:
        calculated[coordinate] = (getGeologicIndex(coordinate, depth, target, calculated) + depth) % EROSION_CONSTANT
    return calculated[coordinate]


def getRisk(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate,int]) -> int:
    return getErosionLevel(coordinate, depth, target, calculated) % 3


def part1(data: Tuple[int,int,int]) -> int:
    depth, targetX, targetY = data
    target = targetX + targetY * 1j
    calculated = {}
    return sum(getRisk(x + y *1j, depth, target, calculated) \
        for x, y in product(range(targetX + 1), range(targetY + 1)))


DIRECTIONS = [ 1, 1j, -1, -1j]
def part2(data: Tuple[int,int,int]) -> int:
    depth, x, y = data
    target = x + y * 1j
    calculated = {}
    final = (x, y, 1)
    queue = [(0, 0, 0, 1)] # 1 = torch, 0 neither, 2 climbing
    bestTimes: Dict[Tuple[int,int,int],int] = dict()
    while queue:
        duration, x, y, risk = heappop(queue)
        coordinate = x + y * 1j
        state = (x, y, risk)
        if state in bestTimes and bestTimes[state] <= duration:
            continue
        if state == final:
            return duration
        bestTimes[state] = duration
        for tool in range(3):
            if tool != risk and tool != getRisk(coordinate, depth, target, calculated):
                heappush(queue, (duration + 7, x, y, tool))
        for direction in DIRECTIONS:
            newCoordinate = coordinate + direction
            if newCoordinate.real >= 0 and newCoordinate.imag >= 0 \
                and getRisk(newCoordinate, depth, target, calculated) != risk:
                heappush(queue, (duration + 1, int(newCoordinate.real), int(newCoordinate.imag), risk))
    raise Exception("Path not found")            


def solve(data: Tuple[int,int,int]) -> Tuple[int,int]:
    return (
        part1(data),
        part2(data)
    )

def getInput(filePath: str) -> Tuple[int,int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return tuple(map(int, re.findall(r"\d+", file.read())))


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