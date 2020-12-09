#! /usr/bin/python3

from common import getInput


def getWeakness(numbers, targetNumber):
    for startIndex in range(0, len(numbers)):
        currentSum = 0
        length = 1
        while currentSum < targetNumber:
            newSet = numbers[startIndex:startIndex + length]
            currentSum = sum(newSet)
            if currentSum == targetNumber:
                weakness = min(newSet) + max(newSet)
                return weakness, newSet
            length += 1
     


def main():
    numbers = list(getInput())
    targetNumber = 22406676
    weakness, resultSet = getWeakness(numbers, targetNumber)
    print("Weakness:", weakness)
    print("Set:", resultSet)
               


if __name__ == "__main__":
    main()
