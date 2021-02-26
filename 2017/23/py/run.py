#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Instruction = List[str]


def part2(number: int) -> int:
    total =  number * 100 + 100000
    nonPrimes = 0
    for candidate in range(total, total + 17000 + 1, 17):
        divider = 2
        while candidate % divider != 0:
            divider += 1
        nonPrimes += candidate != divider
    return nonPrimes


def solve(number: int) -> Tuple[int,int]:
    return (
        (number - 2) ** 2,
        part2(number)
    )


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.readlines()[0].split(" ")[2])


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