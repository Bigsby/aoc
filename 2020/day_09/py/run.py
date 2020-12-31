#! /usr/bin/python3

import sys, os, time


def hasValidPair(numberIndex, numbers):
    number = numbers[numberIndex]
    for testindex in range(numberIndex - 25, numberIndex):
        testNumber = numbers[testindex]
        for pairIndex in range(numberIndex - 25, numberIndex):
            if pairIndex == testindex:
                continue
            if testNumber + numbers[pairIndex] == number:
                return True
    return False


def part1(puzzleInput):
    numbers = puzzleInput
    for index in range(25, len(numbers)):
        if not hasValidPair(index, numbers):
            return numbers[index]


def getWeakness(numbers, targetNumber):
    for startIndex in range(0, len(numbers)):
        currentSum = 0
        length = 1
        while currentSum < targetNumber:
            newSet = numbers[startIndex:startIndex + length]
            currentSum = sum(newSet)
            if currentSum == targetNumber:
                weakness = min(newSet) + max(newSet)
                return weakness
            length += 1


part1Result = 1
def part2(puzzleInput):
    numbers = puzzleInput
    return getWeakness(numbers, part1Result)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line) for line in file.readlines() ]


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