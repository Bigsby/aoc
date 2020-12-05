import sys, os, re


lineRegex = re.compile("^(\d+)x(\d+)x(\d+)$")

def parseLine(line):
    match = lineRegex.match(line)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))

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
            yield parseLine(line)
