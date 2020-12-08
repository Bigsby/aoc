#! /usr/bin/python3

from functools import reduce

from common import getInput, getPeople, getPossibleArrangements, calculateMaximumHappiness, Entry



def main():
    entries = list(getInput())
    people = getPeople(entries)
    me = "me"
    for person in people:
        entries.append(Entry(me, "GAIN", 0, person))
        entries.append(Entry(person, "GAIN", 0, me))
    people.append(me)

    possibleArragements = getPossibleArrangements(people)
    result = calculateMaximumHappiness(possibleArragements, entries)
    print("Maximum happinness:", result)



if __name__ == "__main__":
    main()
