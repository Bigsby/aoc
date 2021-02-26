#! /usr/bin/python3

import sys, os, time
from typing import Tuple
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


def solve(data: str) -> Tuple[int,int]:
    return (
        getLength(data, False), 
        getLength(data, True)
    )


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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