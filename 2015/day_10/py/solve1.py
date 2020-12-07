#! /usr/bin/python3

from common import getInput


def getNextValue(value):
    result = ""
    currentChar = value[0]
    currentCharCount = 1
    for c in value[1:]:
        if c == currentChar:
            currentCharCount = currentCharCount + 1
            continue
        result = result + str(currentCharCount) + str(currentChar)
        currentChar = c
        currentCharCount = 1
    result = result + str(currentCharCount) + str(currentChar)
    return result


def main():
    currentValue = getInput()
    for turn in range(0, 40):
        currentValue = getNextValue(currentValue)
    print("Result length:", len(currentValue))

if __name__ == "__main__":
    main()
