#! /usr/bin/python3

from functools import reduce

from common import getInput


def main():
    rules, myTicket, tickets = getInput()

    validNumbers = {}

    for rule in rules:
        for number in range(rule[1], rule[2] + 1):
            validNumbers[number] = True
        for number in range(rule[3], rule[4] + 1):
            validNumbers[number] = True

    validTickets = []
    for ticket in tickets:
        if all(number in validNumbers for number in ticket):
            validTickets.append(ticket)

    fieldPositions = {}
    rangeField = "range"
    positionsField = "positions"

    def purge(fields, ownerName, index):
        for fieldName in fields:
            if fieldName != ownerName:
                fieldPositions = fields[fieldName][positionsField]
                if index in fieldPositions:
                    fieldPositions.remove(index)
                    if len(fieldPositions) == 1:
                        purge(fields, fieldName, fieldPositions[0])

    for rule in rules:
        fieldPositions[rule[0]] = {
            rangeField: (rule[1], rule[2], rule[3], rule[4]),
            positionsField: [ i for i in range(0, len(rules)) ]
        }

    for ticket in validTickets:
        for index, number in enumerate(ticket):
            for fieldName in fieldPositions:
                fieldRecord = fieldPositions[fieldName]
                if not index in fieldRecord[positionsField]:
                    continue

                rule = fieldRecord[rangeField]
                if number < rule[0] or (number > rule[1] and number < rule[2]) or number > rule[3]:
                    fieldRecord[positionsField].remove(index)
                    if len(fieldRecord[positionsField]) == 1:
                        purge(fieldPositions, fieldName, fieldRecord[positionsField][0])

                                
    departureFieldIndexes = [ fieldPositions[fieldName][positionsField][0] for fieldName in fieldPositions if fieldName.startswith("departure") ]
    result = reduce(lambda soFar, index: soFar * myTicket[index], departureFieldIndexes, 1)
     
    print("Result:", result)


if __name__ == "__main__":
    main()
