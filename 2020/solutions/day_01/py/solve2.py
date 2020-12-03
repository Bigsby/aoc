#! /usr/bin/python3

import sys, os
import itertools



def main():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    if not os.path.isfile(inputFilePath):
        print("File not found")
        sys.exit(1)

    numbers = []
    try:
        with open(inputFilePath) as inputFile:
            for line in inputFile.readlines():
                numbers.append(int(line))
    except Exception as ex:
        print("Error reading file")
        print(ex.args[0])
        sys.exit(1)

    for combination in itertools.combinations(numbers, 2):
        numberA, numberB = combination
        numberToFind = 2020 - numberA - numberB
        if numberToFind in numbers:
            print("Numbers are", numberA, numberB, numberToFind)
            print("Product is", numberA * numberB * numberToFind)
            sys.exit(0)


if __name__ == "__main__":
    main()
