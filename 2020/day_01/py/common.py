import sys, os
from typing import List

def getNumbers() -> List[int]: 
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    if not os.path.isfile(inputFilePath):
        print("File not found")
        sys.exit(1)

    numbers = []
    try:
        with open(inputFilePath) as inputFile:
            for line in inputFile.readlines():
                numbers.append(int(line))
    except Exception as ex:
        print("Error reading file")
        print(ex.args[0])
        sys.exit(1)

    return numbers
