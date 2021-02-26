#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def part1(numbers: List[int]) -> int:
    count = 0
    previous = numbers[-1]
    for number in numbers:
        if number == previous:
            count += number
        previous = number
    return count


def part2(numbers: List[int]) -> int:
    listLength = len(numbers)
    halfLength = listLength // 2
    numbers += numbers
    count = 0
    for index in range(listLength):
        if numbers[index] == numbers[index + halfLength]:
            count += numbers[index]
    return count


def solve(numbers: List[int]) -> Tuple[int,int]:
    return (
        part1(numbers),
        part2(numbers)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(c) for c in file.read().strip() ]


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