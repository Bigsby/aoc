#! /usr/bin/python3

from functools import reduce

from common import getInput


def main():
    numbers = getInput()
    result = reduce(lambda soFar, number: soFar + number, numbers)
    print("Result:", result)


if __name__ == "__main__":
    main()
