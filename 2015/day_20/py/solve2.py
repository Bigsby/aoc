#! /usr/bin/python3

from common import getInput


def getDivisors(number):
    for i in range(1, int(number / 2) + 1):
        if number % i == 0:
            yield i
    yield number


def getPresentCountForHouse(number):
    divisors = list(getDivisors(number))
    presents = 0
    for divisor in getDivisors(number):
        if number / divisor < 50:
            presents += divisor *11
    return presents


def main():
    target = int(getInput())
    houseNumber = 776160 # result from part 1
    step = 1
    presentsReceived = 0

    while presentsReceived <= target:
        houseNumber += step
        presentsReceived = getPresentCountForHouse(houseNumber)
        print('\r', end='') 
        print("House:", houseNumber, "presents:", presentsReceived, end="")
        
    print()


if __name__ == "__main__":
    main()
