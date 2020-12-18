import sys, os, re

parenRegex = re.compile(r"\((?P<expression>[^()]+)\)")
plusRegex = re.compile(r"(?P<first>\d+)\s\+\s(?P<second>\d+)")


def getNextToken(line):
    currentToken = ""
    for index, c in enumerate(line):
        if c == " ":
            return currentToken, line[index + 1:].strip()
        if currentToken.isdigit() and not c.isdigit():
            return currentToken, line[index:].strip()
        currentToken = "".join([currentToken, c])
    return currentToken, ""
        

def performOperation(first, operation, second):
    if operation == "*":
        return first * second
    if operation == "+":
        return first + second
    raise Exception(f"Unknow operation {operation}")
        

def evaluateExpression(text, addFirst):
    match = parenRegex.search(text)
    while match:
        text = "".join([text[:match.start()], str(evaluateExpression(match.group("expression"), addFirst)), text[match.end():]])
        match = parenRegex.search(text)

    if addFirst:
        match = plusRegex.search(text)
        while match:
            text = "".join([text[:match.start()], str(int(match.group("first")) + int(match.group("second"))), text[match.end():]])
            match = plusRegex.search(text)

    token, text = getNextToken(text)
    currentValue = int(token)
    operationToPeform = None
    while text:
        token, text = getNextToken(text)
        if token.isdigit():
            currentValue = performOperation(currentValue, operationToPeform, int(token))
        else:
            operationToPeform = token
    return currentValue
    

def getInput(addFirst = False):
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            yield evaluateExpression(line, addFirst)
