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
    
    def getMoonDelta(self, otherMoon: Coordinates) -> Coordinates:
        return (
            Moon.getDelta(self.position[0], otherMoon[0]),
            Moon.getDelta(self.position[1], otherMoon[1]),
            Moon.getDelta(self.position[2], otherMoon[2])
        )
    
    @staticmethod
    def sum(one: Coordinates, two: Coordinates) -> Coordinates:
        return (one[0] + two[0], one[1] + two[1], one[2] + two[2])

    def updateVelocity(self, otherMoon: Coordinates):
        self.velocity = Moon.sum(self.velocity, self.getMoonDelta(otherMoon))
    
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


def buildStateForCoordinate(coordinate: int, moons: List[Moon]) -> Tuple[Tuple[int,...],Tuple[int,...]]:
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


def solve(moons: List[Moon]) -> Tuple[int,int]:
    return (
        part1(moons),
        part2(moons)
    )


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()