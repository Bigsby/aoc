#! /usr/bin/python3

import sys, os, re

lineReEx = re.compile("^(\d+)-(\d+)\s([a-z]):\s(.*)$")

def countOccurences(password: str, letter: str) -> int:
    count = 0
    for c in password:
        if c == letter:
            count = count + 1
    return count

def isLineValid(line: str) -> bool:
    
    match = lineReEx.match(line)
    if match:
        minimum, maximum, letter, password = match.group(1, 2, 3, 4)
        occurenceCount = countOccurences(password, letter) 
        return occurenceCount >= int(minimum) and occurenceCount <= int(maximum)
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
