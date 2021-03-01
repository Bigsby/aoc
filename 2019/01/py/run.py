#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def get_fuel(mass: int) -> int:
    total = 0
    current_mass = mass
    while True:
        fuel = current_mass // 3 - 2
        if fuel <= 0:
            return total
        total += fuel
        current_mass = fuel


def part2(masses: List[int]) -> int:
    return sum(get_fuel(mass) for mass in masses)


def solve(masses: List[int]) -> Tuple[int,int]:
    return (
        sum((mass // 3) - 2 for mass in masses),
        sum(get_fuel(mass) for mass in masses)
    )

def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ int(line) for line in file.readlines() ]


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