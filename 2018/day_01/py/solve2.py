#! /usr/bin/python3

from common import getInput


def main():
    changes = list(getInput())
    changesLength = len(changes)
    frequency = 0
    previous = set() 
    index = 0
    while frequency not in previous:
        previous.add(frequency)
        frequency += changes[index]
        index = (index + 1) % changesLength


    print("Result:", frequency)


if __name__ == "__main__":
    main()
