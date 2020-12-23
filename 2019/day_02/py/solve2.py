#! /usr/bin/python3

from itertools import product

from common import getInput, runProgram


def main():
    memory = list(getInput())
    expectedValue = 19690720

    values = [ i for i in range(100) ]

    for noun, verb in product(values, repeat=2):
        result = runProgram(list(memory), noun, verb)
        if result == expectedValue:
            print("Result:", 100 * noun + verb)


if __name__ == "__main__":
    main()
