import sys, os, re


instructionRegex = re.compile("^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$")

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            match = instructionRegex.match(line)
            if match:
                yield (match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)))
            else:
                raise Exception("Unrecognized instruction:", line)
