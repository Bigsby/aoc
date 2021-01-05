#! /usr/bin/python3

import sys, os, time
from typing import List, Dict, Set, Tuple
from itertools import product


def getManhatanDistance(locationA: complex, locationB: complex) -> int:
    return int(abs(locationA.real - locationB.real) + abs(locationA.imag - locationB.imag))


def getMapEdges(locations: List[complex]) -> Tuple[int, int, int, int]:
    return  int(min(map(lambda i: i.real, locations))) - 1, \
            int(max(map(lambda i: i.real, locations))) + 1, \
            int(min(map(lambda i: i.imag, locations))) - 1, \
            int(max(map(lambda i: i.imag, locations))) + 1


def findClosestLocation(mapLocation: complex, locations: List[complex]) -> int:
    closest = -1
    closesDistance = sys.maxsize
    for index, location in enumerate(locations):
        distance = getManhatanDistance(mapLocation, location)
        if distance < closesDistance:
            closest = index
            closesDistance = distance
        if distance == closesDistance:
            closest -1
    return closest


def part1(locations: List[complex]):
    startX, endX, startY, endY = getMapEdges(locations)
    mapLocations: Dict[complex,int] = {}
    locationCounts: List[int] = [ 0 for _ in range(len(locations))]

    for mapLocationX, mapLocationY in product(range(startX, endX + 1), range(startY, endY + 1)):
        mapLocation = mapLocationX + mapLocationY * 1j
        closest = findClosestLocation(mapLocation, locations)
        mapLocations[mapLocation] = closest
        if closest != -1:
            locationCounts[closest] += 1
    
    edgeLocations: Set[int] = set()
    for y in range(startY, endY + 1):
        edgeLocations.add(mapLocations[startX + y * 1j])
        edgeLocations.add(mapLocations[endX + y * 1j])
    for x in range(startX, endX + 1):
        edgeLocations.add(mapLocations[x + startY * 1j])
        edgeLocations.add(mapLocations[x + endY * 1j])
    
    return max([ value for index, value in enumerate(locationCounts) if index not in edgeLocations ])


MAX_DISTANCE = 10000
def part2(locations: List[complex]):
    startX, endX, startY, endY = getMapEdges(locations)
    validLocationsCount = 0
    for mapLocationX, mapLocationY in product(range(startX, endX + 1), range(startY, endY + 1)):
        mapLocation = mapLocationX + mapLocationY * 1j
        totalDistances = sum(map(lambda location: getManhatanDistance(location, mapLocation), locations))
        if totalDistances < MAX_DISTANCE:
            validLocationsCount += 1
    return validLocationsCount


def parseLine(line: str) -> complex:
    splitLine: List[str] = line.split(",")
    return int(splitLine[0].strip()) + int(splitLine[1].strip()) * 1j


def getInput(filePath: str):
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