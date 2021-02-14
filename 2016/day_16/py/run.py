#! /usr/bin/python3

import sys, os, time


def getChecksum(data: str, diskLength: int) -> str:
    while len(data) < diskLength:
        data = "0".join([ data, "".join([ "1" if c == "0" else "0" for c in data[::-1] ]) ])
    data = data[:diskLength]
    while len(data) % 2 == 0:
        data = "".join([ "1" if data[index] == data[index + 1] else "0" for index in range(0, len(data), 2) ])
    return data


def part1(data: str) -> str:
    return getChecksum(data, 272)


def part2(data: str) -> str:
    return getChecksum(data, 35651584)


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