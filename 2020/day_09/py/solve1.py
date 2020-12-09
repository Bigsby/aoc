#! /usr/bin/python3

from common import getInput


def hasValidPair(numberIndex, numbers):
    number = numbers[numberIndex]
    for testindex in range(numberIndex - 25, numberIndex):
        testNumber = numbers[testindex]
        for pairIndex in range(numberIndex - 25, numberIndex):
            if pairIndex == testindex:
                continue
            if testNumber + numbers[pairIndex] == number:
                return True
    return False



def main():
    numbers = list(getInput())

    for index in range(25, len(numbers)):
        if not hasValidPair(index, numbers):
            print("First to fail is", numbers[index])
            break


    


if __name__ == "__main__":
    main()
