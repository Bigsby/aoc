#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple, Set
import re

CENTER_OF_MASS = "COM"


def part1(planetOrbits: Dict[str, str]) -> int:
    planets: Set[str] = set()
    for orbited, orbiter in planetOrbits.items():
        planets.add(orbited)
        planets.add(orbiter)
    orbitCounts: Dict[str, int] = { CENTER_OF_MASS: 0 }
    while len(orbitCounts) != len(planets):
        for planet in planets:
            if planet in orbitCounts:
                continue
            if planet in planetOrbits:
                orbitedPlanet = planetOrbits[planet]
                if orbitedPlanet in orbitCounts:
                    orbitCounts[planet] = orbitCounts[orbitedPlanet] + 1
            else:
                orbitCounts[planet] = 1
    return sum(orbitCounts.values())


def getPathToCenterOfMass(planet:str, planetOrbits: Dict[str, str]) -> List[str]:
    route: List[str] = []
    while planet != CENTER_OF_MASS:
        planet = planetOrbits[planet]
        route.append(planet)
    return route


YOU = "YOU"
SAN = "SAN"
def part2(planetOrbits: Dict[str, str]):
    youPath: List[str] = getPathToCenterOfMass(YOU, planetOrbits)
    sanPath: List[str] = getPathToCenterOfMass(SAN, planetOrbits)
    youPath.reverse()
    sanPath.reverse()
    while youPath[0] == sanPath[0]:
        del youPath[0]
        del sanPath[0]
    return len(youPath) + len(sanPath)



lineRegex = re.compile(r"^(?P<first>[A-Z\d]{3})\)(?P<second>[A-Z\d]{3})$")
def parseLine(line: str) -> Tuple[str, str]:
    match = lineRegex.match(line)
    if match:
        return match.group(1), match.group(2)
    else:
        raise Exception("Unmatched line", line)


def getInput(filePath: str) -> Dict[str, str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return {  orbiter: orbited for orbited, orbiter in map(lambda line:  parseLine(line), file.readlines()) }


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