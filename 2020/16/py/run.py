#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Set, Tuple
import re
from functools import reduce

Ticket = List[int]
Rule = Tuple[str,int,int,int,int]


def getValidNumbers(rules: List[Rule]) -> Set[int]:
    validNumbers = set()
    for _, startOne, endOne, startTwo, endTwo in rules:
        for number in range(startOne, endOne + 1):
            validNumbers.add(number)
        for number in range(startTwo, endTwo + 1):
            validNumbers.add(number)
    return validNumbers


def part1(tickets: List[Ticket], validNumbers: Set[int]) -> int:
    invalidNumbers = []
    for ticket in tickets:
        for number in ticket:
            if number not in validNumbers:
                invalidNumbers.append(number)
    return sum(invalidNumbers)


def part2(rules: List[Rule], myTicket: Ticket, tickets: List[Ticket], validNumbers: Set[int]) -> int:
    validTickets = []
    for ticket in tickets:
        if all(number in validNumbers for number in ticket):
            validTickets.append(ticket)
    ranges: Dict[str,Tuple[int,int,int,int]] = dict()
    positions: Dict[str,Set[int]] = dict()
    names = []
    for name, *fieldRanges in rules:
        ranges[name] = tuple(fieldRanges)
        positions[name] = { i for i in range(0, len(rules)) }
        names.append(name)
    for ticket in validTickets:
        for index, number in enumerate(ticket):
            for fieldName in names:
                if index not in positions[fieldName]:
                    continue
                startOne, endOne, startTwo, endTwo = ranges[fieldName]
                if number < startOne or (number > endOne and number < startTwo) or number > endTwo:
                    toRemove = []
                    positions[fieldName].remove(index)
                    if len(positions[fieldName]) == 1:
                        toRemove.append((fieldName, next(iter((positions[fieldName])))))
                    while len(toRemove):
                        ownerName, positionToRemove = toRemove.pop()
                        for otherFieldName in names:
                            if otherFieldName == ownerName or positionToRemove not in positions[otherFieldName]:
                                continue
                            positions[otherFieldName].remove(positionToRemove)
                            if len(positions[otherFieldName]) == 1:
                                toRemove.append((otherFieldName, next(iter(positions[otherFieldName]))))
    departureFieldIndexes = [ next(iter(positions[fieldName])) for fieldName in names if fieldName.startswith("departure") ]
    result = reduce(lambda soFar, index: soFar * myTicket[index], departureFieldIndexes, 1)
    return result


def solve(puzzleInput: Tuple[List[Rule],Ticket,List[Ticket]]) -> Tuple[int,int]:
    rules, myTicket, tickets = puzzleInput
    validNumbers = getValidNumbers(rules)
    return (
        part1(tickets, validNumbers),
        part2(rules, myTicket, tickets, validNumbers)
    )


fieldRegex = re.compile(r"^(?P<field>[^:]+):\s(?P<r1s>\d+)-(?P<r1e>\d+)\sor\s(?P<r2s>\d+)-(?P<r2e>\d+)$")
ticketRegex = re.compile(r"^(?:\d+\,)+(?:\d+$)")
def getInput(filePath: str) -> Tuple[List[Rule],Ticket,List[Ticket]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        rules = []
        myTicket = []
        tickets = []
        doingRules = True
        doingMyTicket = True
        for line in file.readlines():
            if doingRules:
                fieldMatch = fieldRegex.match(line)
                if fieldMatch:
                   rules.append((fieldMatch.group("field"), int(fieldMatch.group("r1s")), int(fieldMatch.group("r1e")), int(fieldMatch.group("r2s")), int(fieldMatch.group("r2e"))))
                else:
                    doingRules = False
            ticketMatch = ticketRegex.match(line)
            if not ticketMatch:
                continue
            if doingMyTicket:
                myTicket = list(map(int, line.split(",")))
                doingMyTicket = False
            else:
                tickets.append(list(map(int, line.split(","))))
        return rules, myTicket, tickets


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()