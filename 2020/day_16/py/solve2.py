#! /usr/bin/python3

from functools import reduce

from common import getInput, getValidNumbers


def main():
    rules, myTicket, tickets = getInput()

    validNumbers = getValidNumbers(rules)

    validTickets = []
    for ticket in tickets:
        if all(number in validNumbers for number in ticket):
            validTickets.append(ticket)

    fields = {}
    rangeField = "range"
    positionsField = "positions"

    def purge(ownerName, index):
        for fieldName in fields:
            fieldPositions = fields[fieldName][positionsField]
            if fieldName != ownerName and index in fieldPositions:
                fieldPositions.remove(index)
                if len(fieldPositions) == 1:
                    purge(fieldName, fieldPositions[0])

    for rule in rules:
        fields[rule[0]] = {
            rangeField: (rule[1], rule[2], rule[3], rule[4]),
            positionsField: [ i for i in range(0, len(rules)) ]
        }

    for ticket in validTickets:
        for index, number in enumerate(ticket):
            for fieldName in fields:
                field = fields[fieldName]
                if not index in field[positionsField]:
                    continue

                rule = field[rangeField]
                if number < rule[0] or (number > rule[1] and number < rule[2]) or number > rule[3]:
                    field[positionsField].remove(index)
                    if len(field[positionsField]) == 1:
                        purge(fieldName, field[positionsField][0])

                                
    departureFieldIndexes = [ fields[fieldName][positionsField][0] for fieldName in fields if fieldName.startswith("departure") ]
    result = reduce(lambda soFar, index: soFar * myTicket[index], departureFieldIndexes, 1)
     
    print("Result:", result)


if __name__ == "__main__":
    main()
