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


def main():
    adapters = sorted(getInput())
    combinations = list(getCombinations(0, adapters))

    print()
    print("Count:", len(combinations))




if __name__ == "__main__":
    main()
