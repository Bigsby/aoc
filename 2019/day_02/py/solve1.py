#! /usr/bin/python3

from common import getInput, runProgram


def main():
    memory = list(getInput())
    result = runProgram(memory, 12, 2)
    print("Result:", result)


if __name__ == "__main__":
    main()
