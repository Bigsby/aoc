#! /usr/bin/python3

from common import getInput


def getPossibleAdapters(joltage, adapters):
    for index in range(len(adapters)):
        newJoltage = adapters[index]
        if newJoltage - joltage < 4:
            yield newJoltage, adapters[index + 1:]


def getCombinations(joltage, adapters, previous = []):
#    input(f"c {previous} {joltage} {adapters}")
    for nextJoltage, adaptersLeft in getPossibleAdapters(joltage, adapters):
        previous.append(nextJoltage)
        if len(adaptersLeft) == 0:
            yield previous
        else:
            for combination in getCombinations(nextJoltage, adaptersLeft, previous[:]):
                yield combination

def calculateCombinations(sequence):
    if sequence == 1 or sequence == 2:
        return 1
    if sequence == 3:
        return 2
    return calculateCombinations(sequence - 1) + calculateCombinations(sequence - 2) + calculateCombinations(sequence - 3)

def buildAdapters(length):
    adapters = []
    for i in range(length):
        adapters.append(3 + i)
    return adapters
        

def main():
#    adapters = sorted(getInput())
#    combinations = list(getCombinations(0, adapters))
#
    for length in range(2, 20):
        adapters = buildAdapters(length)
        combinations = list(getCombinations(0, adapters))
        calculated = calculateCombinations(length)
        print("Length:", length, "\tCombinations:", len(combinations),"\tCalculated:", calculated)
#    print("Adapters:", len(adapters))
#    print("Count:", len(combinations))




if __name__ == "__main__":
    main()
