#! /usr/bin/python3

import sys
from itertools import combinations
import itertools

from common import getNumbers

def main():
    numbers = getNumbers()

    for combination in combinations(numbers, 2):
        numberA, numberB = combination
        numberToFind = 2020 - numberA - numberB
        if numberToFind in numbers:
            print("Numbers are", numberA, numberB, numberToFind)
            print("Product is", numberA * numberB * numberToFind)
            sys.exit(0)


if __name__ == "__main__":
    main()
