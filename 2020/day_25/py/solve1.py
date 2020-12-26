#! /usr/bin/python3

from common import getInput

baseSubjectNumber = 7
divider = 20201227

def getNextValue(value, subjectNumber = baseSubjectNumber):
    return (value * subjectNumber) % divider

def getLoopSize(target):
    value = 1
    cycle = 0
    while value != target:
        cycle += 1
        value = getNextValue(value)
    return cycle


def transform(subjectNumber, cycles):
    value = 1
    while cycles:
        cycles -= 1
        value = getNextValue(value, subjectNumber)
    return value


def main():
    card, door = getInput()
    doorLoopSize = getLoopSize(door)
    encrytionKey = transform(card, doorLoopSize)
    print("Encryption key:", encrytionKey)
    



if __name__ == "__main__":
    main()
