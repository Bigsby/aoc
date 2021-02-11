#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from functools import reduce

Bus = Tuple[int,int]

def part1(puzzleInput: Tuple[int,List[Bus]]) -> int:
    timestamp, busses = puzzleInput
    closestAfter = sys.maxsize
    closestBus = None
    for bus in busses:
        timeAfter = (timestamp // bus[0] + 1) * bus[0] - timestamp
        if timeAfter < closestAfter:
            closestAfter = timeAfter
            closestBus = bus
    if closestBus:
        return closestAfter * closestBus[0]
    raise Exception("Closest bus not found")


def modularMultiplicativeInverse(a: int, b:int) -> int:
    q = a % b
    for i in range(1, b):
        if ((q * i) % b) == 1:
            return i
    return 1


def part2(puzzleInput: Tuple[int,List[Bus]]) -> int:
    _, busses = puzzleInput
    product = reduce(lambda soFar, bus: soFar * bus[0], busses, 1)
    sum = 0
    for bus in busses:
        currentProduct = product // bus[0]
        sum += ((bus[0] - bus[1]) % bus[0]) * currentProduct * modularMultiplicativeInverse(currentProduct, bus[0])
    return sum % product


def getInput(filePath: str) -> Tuple[int,List[Bus]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        lines = file.readlines()
        return int(lines[0]), [ (int(busId), index) for index, busId in enumerate(lines[1].split(",")) if  busId != "x" ]


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