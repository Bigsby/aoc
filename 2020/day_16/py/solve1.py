#! /usr/bin/python3

from common import getInput, getValidNumbers


def main():
    rules, myTicket, tickets = getInput()

    validNumbers = getValidNumbers(rules)

    invalidNumbers = []
    for ticket in tickets:
        for number in ticket:
            if not number in validNumbers:
                invalidNumbers.append(number)

    print("Result:", sum(invalidNumbers))


if __name__ == "__main__":
    main()
