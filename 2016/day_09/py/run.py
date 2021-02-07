#! /usr/bin/python3

import sys, os, time
import re


markerRegex = re.compile(r"(?P<prior>[A-Z]*)\((?P<length>\d+)x(?P<repeats>\d+)\)(?P<data>.*)")
def getLength(data: str, recursive: bool) -> int:
    match = markerRegex.match(data)
    if match:
        dataLength = int(match.group("length"))
        data = match.group("data")
        return len(match.group("prior")) + \
            int(match.group("repeats")) * (getLength(data[:dataLength], True) if recursive else dataLength) + \
            getLength(data[dataLength:], recursive)
    else:
        return len(data)


def part1(data: str) -> int:
    return getLength(data, False)


def part2(data: str) -> int:           
    return getLength(data, True)


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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