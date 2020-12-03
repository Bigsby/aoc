#! /usr/bin/python3

import sys

from common import getNumbers

def main():
    numbers = getNumbers()

    for number in numbers:
        numberToFind = 2020 - number
        if numberToFind in numbers:
            print("Found", number, "and", numberToFind)
            print("Product is", number * numberToFind)
            sys.exit(0)


if __name__ == "__main__":
    main()
