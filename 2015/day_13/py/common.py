import sys, os, re
from enum import Enum
from itertools import permutations


lineRegex = re.compile(r"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$")

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


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                yield Entry(match.group(1), match.group(2), match.group(3), match.group(4))
