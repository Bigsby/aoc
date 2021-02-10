#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re, math
from copy import deepcopy
from itertools import combinations
from functools import reduce

Coordinates = Tuple[int,int,int]


class Moon():
    def __init__(self, x: int, y: int, z: int):
        self.position: Coordinates = (x, y, z)
        self.velocity: Coordinates = (0, 0, 0)

    @staticmethod    
    def getDelta(thisValue: int, otherValue: int) -> int: 
        if thisValue < otherValue:
            return 1
        if thisValue > otherValue:
            return -1
        return 0
    
    @staticmethod
    def sum(one: Coordinates, two: Coordinates) -> Coordinates:
        return tuple(map(sum, zip(one, two)))

    def updateVelocity(self, otherMoon: Coordinates):
        self.velocity = Moon.sum(self.velocity, tuple(Moon.getDelta(self.position[coordinate], otherMoon[coordinate]) for coordinate in range(3)))
    
    def updatePosition(self):
        self.position = Moon.sum(self.position, self.velocity)

    def getTotalEnergy(self) -> int:
        return sum(map(abs, self.position)) * sum(map(abs, self.velocity))

    def __str__(self):
        return f"{self.position} {self.velocity}"
    def __repr__(self) -> str:
        return self.__str__()


def runStep(moons: List[Moon]):
    for moonA, moonB in combinations(moons, 2):
        moonA.updateVelocity(moonB.position)
        moonB.updateVelocity(moonA.position)
    for moon in moons:
        moon.updatePosition()


def part1(moons: List[Moon]) -> int:
    step = 1000
    moons = deepcopy(moons)
    while step:
        step -= 1
        runStep(moons)
    return sum(map(lambda moon: moon.getTotalEnergy(), moons))


def buildStateForCoordinate(coordinate: int, moons: List[Moon]) -> Tuple[Tuple[int],Tuple[int]]:
    return (tuple(moon.position[coordinate] for moon in moons), tuple(moon.velocity[coordinate] for moon in moons))


def part2(moons: List[Moon]) -> int:
    step = 0
    initialStates = [ buildStateForCoordinate(coordinate, moons) for coordinate in range(3)]
    cyles = [ 0 ] * 3
    while not all(cyles):
        step += 1
        runStep(moons)
        for coordinate in range(3):
            if not cyles[coordinate]:
                currentState = buildStateForCoordinate(coordinate, moons)
                if currentState == initialStates[coordinate]:
                    cyles[coordinate] = step
    return reduce(lambda soFar, cycle: soFar * cycle // math.gcd(soFar, cycle), cyles)


lineRegex = re.compile(r"^<x=(?P<x>-?\d+),\sy=(?P<y>-?\d+),\sz=(?P<z>-?\d+)>$")
def parseLine(line: str) -> Moon:
    match = lineRegex.match(line)
    if match:
        return Moon(int(match.group("x")), int(match.group("y")), int(match.group("z")))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Moon]:
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