#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple, Set
import re

CENTER_OF_MASS = "COM"


def part1(planet_orbits: Dict[str, str]) -> int:
    planets: Set[str] = set()
    for orbiter, orbited in planet_orbits.items():
        planets.add(orbited)
        planets.add(orbiter)
    orbit_counts: Dict[str, int] = { CENTER_OF_MASS: 0 }
    while len(orbit_counts) != len(planets):
        for planet in planets:
            if planet in orbit_counts:
                continue
            if planet in planet_orbits:
                orbited_planet = planet_orbits[planet]
                if orbited_planet in orbit_counts:
                    orbit_counts[planet] = orbit_counts[orbited_planet] + 1
            else:
                orbit_counts[planet] = 1
    return sum(orbit_counts.values())


def get_path_to_center_of_mass(planet:str, planet_orbits: Dict[str, str]) -> List[str]:
    route: List[str] = []
    while planet != CENTER_OF_MASS:
        planet = planet_orbits[planet]
        route.append(planet)
    return route


YOU = "YOU"
SAN = "SAN"
def part2(planet_orbits: Dict[str, str]):
    you_path: List[str] = get_path_to_center_of_mass(YOU, planet_orbits)
    san_path: List[str] = get_path_to_center_of_mass(SAN, planet_orbits)
    you_path.reverse()
    san_path.reverse()
    while you_path[0] == san_path[0]:
        del you_path[0]
        del san_path[0]
    return len(you_path) + len(san_path)


def solve(planet_orbits: Dict[str, str]) -> Tuple[int,int]:
    return (
        part1(planet_orbits),
        part2(planet_orbits)
    )


line_regex = re.compile(r"^(?P<orbited>[A-Z\d]{3})\)(?P<orbiter>[A-Z\d]{3})$")
def parseLine(line: str) -> Tuple[str, str]:
    match = line_regex.match(line)
    if match:
        return match.group("orbited"), match.group("orbiter")
    else:
        raise Exception("Unmatched line", line)


def get_input(file_path: str) -> Dict[str, str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return {  orbiter: orbited for orbited, orbiter in map(lambda line:  parseLine(line), file.readlines()) }


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()