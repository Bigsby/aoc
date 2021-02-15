#! /usr/bin/python3

import sys, os, time


def part1(steps: int) -> int:
    spinLock = [ 0 ]
    position = 0
    for number in range(1, 2017 + 1):
        position = (position + steps) % len(spinLock) + 1
        spinLock.insert(position, number)
    return spinLock[position + 1]


def part2(steps: int) -> int:
    position = 0
    result = 0
    for number in range(1, 5 * 10 ** 7 + 1):
        position = ((position + steps) % number) + 1
        if (position == 1):
            result = number
    return result


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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