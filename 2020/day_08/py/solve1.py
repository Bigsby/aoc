#! /usr/bin/python3

from common import getInput, testBoot


def main():
    ops = list(getInput())
    success, accumulator = testBoot(ops)

    print("Accumulator value:", accumulator)

        


if __name__ == "__main__":
    main()
