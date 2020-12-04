import sys, os, re
from typing import List, Tuple

lineReEx = re.compile("^(\d+)-(\d+)\s([a-z]):\s(.*)$")

def getLines() -> List[Tuple[int,int,str,str]]:
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    inputFilePath = sys.argv[1]
    if not os.path.isfile(inputFilePath):
        print("File not found")
        sys.exit(1)

    with open(inputFilePath) as file:
        for line in file.readlines():
            match = lineReEx.match(line)
            if match:
                min, max, letter, password = match.group(1, 2, 3, 4)
                yield (int(min), int(max), letter, password)
            
