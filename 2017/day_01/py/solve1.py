#! /usr/bin/python3

from common import getInput


def main():
    count = 0
    numbers = list(getInput())
    previous = numbers[-1]
    for number in numbers:
        if number == previous:
            count += number
        previous = number

    print("Result:", count)


if __name__ == "__main__":
    main()
