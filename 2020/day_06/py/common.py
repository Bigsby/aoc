import sys, os
from string import ascii_lowercase


def addToLetterCount(record, letter):
    if letter in record:
        record[letter] = record[letter] + 1
    else:
        record[letter] = 1


def processGroupEntry(groupEntry):
    record = {}
    peopleCount = 0
    for line in groupEntry.split("\n"):
        if line:
            peopleCount = peopleCount + 1
        for c in line:
            addToLetterCount(record, c)
    return {
        "peopleCount": peopleCount,
        "answers": record
        }
        

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath) as file:
        contents = file.read()
        groupEntries = contents.split("\n\n")
        for groupEntry in groupEntries:
            yield processGroupEntry(groupEntry)

