#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum
from itertools import permutations


class Balance(Enum):
    GAIN = 1
    LOSS = 2


class Entry():
    def __init__(self, target, balance, value, source):
        self.target = target
        self.source = source
        self.balance = Balance.GAIN if balance == "gain" else Balance.LOSS
        self.value = int(value)

    def __str__(self):
        return f"{self.target} {self.balance} {self.value} {self.source}"
    def __repr__(self):
        return self.__str__()


def getEntryValue(target, source, entries):
    entry = next(filter(lambda e: e.target == target and e.source == source, entries))
    return entry.value if entry.balance == Balance.GAIN else -entry.value


def calculateHappiness(arrangement, entries):
    total = 0
    length = len(arrangement)
    for index, person in enumerate(arrangement):
        total += getEntryValue(person, arrangement[index - 1], entries)        
        total += getEntryValue(person, arrangement[index + 1 if index < length - 1 else 0], entries)
    return total


def calculateMaximumHappiness(possibleArragements, entries):
    return max(map(lambda arrangement: calculateHappiness(arrangement, entries), possibleArragements))


def getPeople(entries):
    people = set()
    for entry in entries:
        people.add(entry.target)
        people.add(entry.source)
    return list(people)


def getPossibleArrangements(people):
    return permutations(people, len(people))


def part1(puzzleInput):
    entries = puzzleInput
    people = getPeople(entries)
    possibleArragements = getPossibleArrangements(people)
    result = calculateMaximumHappiness(possibleArragements, entries)
    return result


def part2(puzzleInput):
    entries = puzzleInput
    people = getPeople(entries)
    me = "me"
    for person in people:
        entries.append(Entry(me, "GAIN", 0, person))
        entries.append(Entry(person, "GAIN", 0, me))
    people.append(me)

    possibleArragements = getPossibleArrangements(people)
    result = calculateMaximumHappiness(possibleArragements, entries)
    return result


lineRegex = re.compile(r"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$")
def parseLine(line):
    match = lineRegex.match(line)
    return Entry(*match.group(1, 2, 3, 4))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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