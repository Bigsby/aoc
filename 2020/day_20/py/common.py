import sys, os, re


numberLineRegex = re.compile(r"^Tile\s(?P<number>\d+):$")

def calculatBorders(lines):
    width = len(lines[0])
    top = lines[0]
    right = "".join(map(lambda line: line[width - 1], lines))
    bottom = lines[width - 1]
    left = "".join(map(lambda line: line[0], lines))
    return top, right, bottom, left
     

class Tile():
    def __init__(self, number, lines):
        self.number = number
        self.lines = lines
        self.borders = calculatBorders(self.lines)
    def __str__(self):
        return f"{self.number} {self.borders}"
    def __repr__(self):
        return self.__str__()


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        tileNumber = 0
        lines = []
        for line in file.readlines():
            numberMatch = numberLineRegex.match(line)
            if numberMatch:
                tileNumber = int(numberMatch.group("number"))
                lines = []
            elif line.strip() == "":
                yield Tile(tileNumber, lines)
            else:
                lines.append(line.strip())

