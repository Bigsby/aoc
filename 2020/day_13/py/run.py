#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


class Bus():
    def __init__(self, id: int, index: int):
        self.id = id
        self.index = index


def part1(puzzleInput: Tuple[int,List[Bus]]) -> int:
    timestamp, busses = puzzleInput
    closestAfter = sys.maxsize
    closestBus = None
    for bus in busses:
        timeAfter = (timestamp // bus.id + 1) * bus.id - timestamp
        if timeAfter < closestAfter:
            closestAfter = timeAfter
            closestBus = bus

    if closestBus:
        return closestAfter * closestBus.id
    raise Exception("Closest bus not found")



def modularMultiplicativeInverse(a: int, b:int) -> int:
    b0 = b
    x0, x1 = 0, 1
    if b == 1: 
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: 
        x1 += b0
    return x1
 

def getNextIndex(first: Bus, second: Bus) -> int:
    sum = 0
    prod = first.id * second.id
    pFirst = prod // first.id
    pSecond = prod // second.id
    sum = first.index * modularMultiplicativeInverse(pFirst, first.id) * pFirst \
        - second.index * modularMultiplicativeInverse(pSecond, second.id) * pSecond
    return sum % prod


def part2(puzzleInput: Tuple[int,List[Bus]]) -> int:
    _, busses = puzzleInput
    lastBus = busses[0]
    for bus in busses[1:]:
        lastBus = Bus(lastBus.id * bus.id, getNextIndex(lastBus, bus))
    return lastBus.index


def getInput(filePath: str) -> Tuple[int,List[Bus]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        lines = file.readlines()
        return int(lines[0]), [ Bus(int(busId), index) for index, busId in enumerate(lines[1].split(",")) if  busId != "x" ]


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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()