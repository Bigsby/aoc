import sys, os, re


numberRegex = re.compile(r"[^\d](-?[\d]+)")

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        contents = file.read().strip()
        for match in numberRegex.finditer(contents):
            yield int(match.group(1))
