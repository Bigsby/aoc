#! /usr/bin/python3

from common import getInput



def main():
    rules, myTicket, tickets = getInput()

    validNumbers = {}

    for rule in rules:
        for number in range(rule[1], rule[2] + 1):
            validNumbers[number] = True
        for number in range(rule[3], rule[4] + 1):
            validNumbers[number] = True

    invalidNumbers = []
    for ticket in tickets:
        for number in ticket:
            if not number in validNumbers:
                invalidNumbers.append(number)

    print("Result:", sum(invalidNumbers))


if __name__ == "__main__":
    main()
