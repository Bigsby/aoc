import sys, os, re

fieldRegex = re.compile(r"^(?P<field>[^:]+):\s(?P<r1s>\d+)-(?P<r1e>\d+)\sor\s(?P<r2s>\d+)-(?P<r2e>\d+)$")
ticketRegex = re.compile(r"^(?:\d+\,)+(?:\d+$)")


def getValidNumbers(rules):
    validNumbers = set()
    for rule in rules:
        for number in range(rule[1], rule[2] + 1):
            validNumbers.add(number)
        for number in range(rule[3], rule[4] + 1):
            validNumbers.add(number)
    return validNumbers


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        rules = []
        myTicket = None
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
                myTicket = list(map(lambda i: int(i), line.split(",")))
                doingMyTicket = False
            else:
                tickets.append(list(map(lambda i: int(i), line.split(","))))


        return rules, myTicket, tickets




