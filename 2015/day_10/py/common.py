import sys, os


def getNextValue(value):
    result = ""
    currentChar = value[0]
    currentCharCount = 1
    for c in value[1:]:
        if c == currentChar:
            currentCharCount = currentCharCount + 1
            continue
        result = result + str(currentCharCount) + str(currentChar)
        currentChar = c
        currentCharCount = 1
    result = result + str(currentCharCount) + str(currentChar)
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
