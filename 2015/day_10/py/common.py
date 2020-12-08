import sys, os, re


testRegex = re.compile(r"(\d)\1+|\d")

def getNextValue(value):
    matches = testRegex.finditer(value)
    result = ""
    for match in matches:
        group = match.group()
        result = result + str(len(group)) + group[0]
    return result


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        return file.read().strip()
