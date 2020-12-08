#! /usr/bin/python3

from functools import reduce
from itertools import permutations

from common import getInput, Balance

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


def getPeople(entries):
    people = set()
    for entry in entries:
        people.add(entry.target)
        people.add(entry.source)
    return list(people)


def main():
    entries = list(getInput())
    people = getPeople(entries)
    possibleArragements = permutations(people, len(people))
    result = max(map(lambda arrangement: calculateHappiness(arrangement, entries), possibleArragements))
    print("Maximum happinness:", result)



if __name__ == "__main__":
    main()
