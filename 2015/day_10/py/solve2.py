#! /usr/bin/python3

from common import getInput, getNextValue


def main():
    currentValue = getInput()
    for turn in range(0, 50):
        currentValue = getNextValue(currentValue)
    print("Result length:", len(currentValue))

   


if __name__ == "__main__":
    main()
