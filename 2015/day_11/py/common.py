import sys, os, re


aOrd = ord("a")
zOrd = ord("z")
forbiddenLetters = [ ord("i"), ord("o"), ord("l") ]
pairsRegex = re.compile(r"^.*(.)\1{1}.*(.)\2{1}.*$")

def isPasswordValid(password):
    ords = list(map(lambda c: ord(c), password))
    for testOrd in forbiddenLetters:
        if testOrd in ords:
            return False

    if not pairsRegex.match(password):
        return False

    for index in range(0, len(ords) - 2):
        if ords[index] == ords[index + 1] - 1 and ords[index] == ords[index + 2] - 2:
            return True

    return False
    

def getNextPassword(current):
    result = list(current)
    for index in range(len(result) - 1, 0, -1):
        cOrd = ord(result[index])
        if cOrd == zOrd:
            result[index] = chr(aOrd)
            continue
        result[index] = chr(cOrd + 1)
        break
    return "".join(result)


def getNextValidPassword(currentPassword):
    currentPassword = getNextPassword(currentPassword)
    while not isPasswordValid(currentPassword):
        currentPassword = getNextPassword(currentPassword)

    return currentPassword


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
