#! /usr/bin/python3

from functools import reduce

from common import getInput


def main():
    highestId = reduce(lambda currentMax, bp: max(currentMax, bp.id), getInput(), 0)
    print("Highest Id is", highestId)
    

if __name__ == "__main__":
    main()
