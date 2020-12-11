#! /usr/bin/python3

from common import getInput

def getDivisors(number):
    for i in range(1, int(number / 2) + 1):
        if number % i == 0:
            yield i
    yield number


def getPresentCountForHouse(number):
    return sum(getDivisors(number))


def main():
    target = int(getInput() / 10)
    houseNumber = 0 
    presentsReceived = 0
    step = 2 * 3 * 5 * 7 * 11 

    while presentsReceived <= target:
        houseNumber += step
        presentsReceived = getPresentCountForHouse(houseNumber)
        print('\r', end='') 
        print("House:", houseNumber, "presents:", presentsReceived, end="")
        
    print("Lowest house number to target:", houseNumber)


if __name__ == "__main__":
    main()
