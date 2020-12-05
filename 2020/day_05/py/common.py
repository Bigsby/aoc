import sys, os, re

lineRegex = re.compile("^([BF]{7})([LR]{3})$")


class BoardingPass:
    def __init__(self, rowText, columnText):
        self.rowText = rowText
        self.columnText = columnText
        self.row = self.calculateValue(rowText, "F", "B")
        self.column = self.calculateValue(columnText, "L", "R")
        self.id = self.row * 8 + self.column

    def calculateValue(self, text, zero, one):
        value = 0
        for index, c in enumerate(text[::-1]):
            if c == one:
                value = value + pow(2, index)
            elif c != zero:
                raise Exception("Unknown value: " + c)
        return value
            

def processLine(line):
    match = lineRegex.match(line)
    if match:
        return BoardingPass(match.group(1), match.group(2))
    else:
        raise Exception("Bad formatted line: " + line)


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath) as file:
        for line in file.readlines():
            yield processLine(line)            

