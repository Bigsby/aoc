#! /usr/bin/python3

from common import getInput


def main():
    numbers = list(getInput())
    listLength = len(numbers)
    halfLength = listLength // 2
    numbers += numbers
    
    count = 0
    for index in range(listLength):
        if numbers[index] == numbers[index + halfLength]:
            count += numbers[index]

    print("Result:", count)


if __name__ == "__main__":
    main()
