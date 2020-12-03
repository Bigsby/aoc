#! /usr/bin/python3

import sys, os, re

lineReEx = re.compile("^(\d+)-(\d+)\s([a-z]):\s(.*)$")

def isLineValid(line: str) -> bool:
    match = lineReEx.match(line)
    if match:
        first, second, letter, password = match.group(1, 2, 3, 4)
        return (password[int(first) - 1] == letter) ^ (password[int(second) - 1] == letter)
    else:
        raise Exception("Bad formatted line:", line)


def main():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    if not os.path.isfile(inputFilePath):
        print("File not found")
        sys.exit(1)

    validPasswordCount = 0
    try:
        with open(inputFilePath) as inputFile:
            for line in inputFile.readlines():
                if isLineValid(line):
                    validPasswordCount = validPasswordCount + 1

    except Exception as ex:
        print("Error reading file")
        print(ex.args[0])
        sys.exit(1)

    print("Valid password count is", validPasswordCount)


if __name__ == "__main__":
    main()
