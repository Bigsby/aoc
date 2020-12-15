#! /usr/bin/python3

from typing import NamedTuple
from collections import defaultdict

from common import getInput


class LastOccurrences(NamedTuple):
    last: int
    second: int


def main():
    numbers = list(getInput())
    turn = 0
    occurrences = {}
    for number in numbers:
        turn += 1
        occurrences[number] = LastOccurrences(turn, 0)

    lastNumber = numbers[-1]
    
    while turn < 2020:
        turn += 1
        occurrence = occurrences[lastNumber]

        if occurrence.second == 0:
            lastNumber = 0
        else:
            lastNumber = occurrence.last - occurrence.second

        if lastNumber in occurrences:
            lastNumberOccurrences = occurrences.get(lastNumber)
            occurrences[lastNumber] = LastOccurrences(turn, lastNumberOccurrences.last)
        else:
            occurrences[lastNumber] = LastOccurrences(turn, 0)
    
    print("2020th number:", lastNumber)


if __name__ == "__main__":
    main()
