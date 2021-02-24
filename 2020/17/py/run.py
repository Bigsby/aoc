#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, Tuple

Coordinate = Tuple[int,...]
Universe = Dict[Coordinate,bool]


def getLimits(universe: Universe) -> Tuple[Coordinate,Coordinate]:
    lowerLimit = []
    upperLimit = []
    for index in range(len(list(universe.keys())[0])):
        lowerLimit.append(min(key[index] for key in universe.keys()))
        upperLimit.append(max(key[index] for key in universe.keys()))
    return (tuple(lowerLimit), tuple(upperLimit))


OUTER_DIMENSIONS = [ "z", "w" ]
def printUniverse(universe: Universe):
    lowerLimit, upperLimit = getLimits(universe)
    dimensionCount = len(list(universe.keys())[0])
    for coordinate in cycleCoordinates(lowerLimit, upperLimit):
        if coordinate[-1] == lowerLimit[-1] and coordinate[-2] == lowerLimit[-2]:
            print("\n" + ", ".join(OUTER_DIMENSIONS[index] + "=" + str(coordinate[index]) for index in range(dimensionCount - 2)), end="")
        if coordinate[-1] == lowerLimit[-1]:
            print()
        print('#' if universe[coordinate] else '.', end="")
    print()
    input()


def previous(coordinate: Coordinate) -> Coordinate:
    valueList = list(coordinate)
    valueList[-1] -= 1
    return tuple(valueList)


def under(coordinate: Coordinate) -> Coordinate:
    return tuple(v - 1 for v in coordinate)


def over(coordinate: Coordinate) -> Coordinate:
    return tuple(v + 1 for v in coordinate)


def addDimension(coordiate: Coordinate) -> Coordinate:
    return tuple([ 0 ] + list(coordiate))


def nextCoordinateValue(current: Coordinate, lowerLimit: Coordinate, upperLimit: Coordinate) -> Coordinate:
    result = list(current)
    for index in range(len(current) - 1, -1, -1):
        if current[index] < upperLimit[index]:
            result[index] += 1
            for overflow in range(index + 1, len(current)):
                result[overflow] = lowerLimit[overflow]
            break
    return tuple(result)


def cycleCoordinates(lowerLimit: Coordinate, upperLimit: Coordinate) -> Iterable[Coordinate]:
    current = previous(lowerLimit)
    while (current != upperLimit):
        current = nextCoordinateValue(current, lowerLimit, upperLimit)
        yield current


def getNeighborActiveCount(universe: Universe, coordinate: Coordinate) -> int:
    return sum(neighbor != coordinate and neighbor in universe and universe[neighbor] for neighbor in cycleCoordinates(under(coordinate), over(coordinate)))


def nextCycle(universe: Universe) -> Universe:
    newState: Universe = dict()
    lowerLimit, upperLimit = getLimits(universe)
    for coordinate in cycleCoordinates(under(lowerLimit), over(upperLimit)):
        activeNeighborCount = getNeighborActiveCount(universe, coordinate)
        newValue = False
        if coordinate in universe and universe[coordinate]:
            newValue = activeNeighborCount == 2 or activeNeighborCount == 3
        else:
            newValue = activeNeighborCount == 3
        newState[coordinate] = newValue
    return newState


def runCycles(universe: Universe) -> int:
    for _ in range(6):
        universe = nextCycle(universe)
    return sum(universe.values())


def part1(universe: Universe) -> int:
    return runCycles(universe)


def part2(universe: Universe) -> int:
    universe = { addDimension(coordinate): value for coordinate, value in universe.items() }
    return runCycles(universe)


def getInput(filePath: str) -> Universe:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    universe: Universe = dict()
    with open(filePath, "r") as file:
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                universe[(0, y, x)] = c == "#"
    return universe


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