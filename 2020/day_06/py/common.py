import sys, os
from string import ascii_lowercase


def buildGroupRecord():
    record = {}
    for letter in ascii_lowercase:
        record[letter] = 0
    return record


def processGroupEntry(groupEntry):
    record = buildGroupRecord()
    for line in groupEntry.split("\n"):
        for c in line:
            record[c] = 1
    return record
        

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

