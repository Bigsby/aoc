#! /usr/bin/python3

from functools import reduce

from common import getInput


def calculateCombinations(sequence):
    if sequence < 3:
        return 1
    if sequence == 3:
        return 2
    return calculateCombinations(sequence - 1) + calculateCombinations(sequence - 2) + calculateCombinations(sequence - 3)


def main():
    adapters = sorted(getInput())
    adapters.append(adapters[len(adapters) - 1])
    sequences = []
    currentSequenceLength = 1
    currentJoltage = 0
    for joltage in adapters:
        if currentJoltage == joltage - 1:
            currentSequenceLength += 1
        else:
            sequences.append(currentSequenceLength)
            currentSequenceLength = 1
        currentJoltage = joltage

    result = reduce(lambda soFar, length: soFar * calculateCombinations(length), sequences, 1)
    print("Combination count:", result)


if __name__ == "__main__":
    main()
