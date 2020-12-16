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

    for rule in rules:
        fields[rule[0]] = {
            rangeField: (rule[1], rule[2], rule[3], rule[4]),
            positionsField: { i for i in range(0, len(rules)) }
        }

    for ticket in validTickets:
        for index, number in enumerate(ticket):
            for fieldName in fields:
                field = fields[fieldName]
                if index not in field[positionsField]:
                    continue

                rule = field[rangeField]
                if number < rule[0] or (number > rule[1] and number < rule[2]) or number > rule[3]:
                    toRemove = []
                    field[positionsField].remove(index)
                    if len(field[positionsField]) == 1:
                        toRemove.append((fieldName, list(field[positionsField])[0]))

                    while len(toRemove):
                        ownerName, positionToRemove = toRemove.pop()
                        for otherFieldName in fields:
                            otherFieldPositions = fields[otherFieldName][positionsField]
                            if otherFieldName == ownerName or positionToRemove not in otherFieldPositions:
                                continue
                            otherFieldPositions.remove(positionToRemove)
                            if len(otherFieldPositions) == 1:
                                toRemove.append((otherFieldName, list(otherFieldPositions)[0]))


                                
    departureFieldIndexes = [ list(fields[fieldName][positionsField])[0] for fieldName in fields if fieldName.startswith("departure") ]
    result = reduce(lambda soFar, index: soFar * myTicket[index], departureFieldIndexes, 1)
     
    print("Result:", result)


if __name__ == "__main__":
    main()
