#! /usr/bin/python3

from functools import reduce

from common import getInput, getPeople, getPossibleArrangements, calculateMaximumHappiness



def main():
    entries = list(getInput())
    people = getPeople(entries)
    possibleArragements = getPossibleArrangements(people)
    result = calculateMaximumHappiness(possibleArragements, entries)
    print("Maximum happinness:", result)



if __name__ == "__main__":
    main()
