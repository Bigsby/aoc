#! /usr/bin/python3

import sys, os, time
import math


def getDivisors(number):
    large_divisors = []
    for i in range(1, int(math.sqrt(number) + 1)):
        if number % i == 0:
            yield i
            if i*i != number:
                large_divisors.append(number / i)
    for divisor in reversed(large_divisors):
        yield divisor


def getPresentCountForHouse(number):
    return sum(getDivisors(number))


def part1(puzzleInput):
    houseNumber = 0 
    presentsReceived = 0
    step = 2 * 3 * 5 * 7 * 11 
    targetPresents = puzzleInput / 10
    while presentsReceived <= targetPresents:
        houseNumber += step
        presentsReceived = getPresentCountForHouse(houseNumber)
    return houseNumber


def getPresentCountForHouse2(number):
    presents = 0
    for divisor in getDivisors(number):
        if number / divisor < 50:
            presents += divisor * 11
    return presents


part1Result = 1
def part2(puzzleInput):
    houseNumber = part1Result
    step = 1
    presentsReceived = 0
    while presentsReceived <= puzzleInput:
        houseNumber += step
        presentsReceived = getPresentCountForHouse2(houseNumber)
    return houseNumber


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    global part1Result
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