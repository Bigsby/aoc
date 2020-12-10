import sys, os, re


lineRegex = re.compile(r"^(\w+)\s=>\s(\w+)$")


class Replacement():
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return f"{self.source} -> {self.target}"
    def __repr__(self):
        return self.__str__()


def processReplacement(molecule, replacement):
    return processReplacementDirect(molecule, replacement.source, replacement.target)

    
def processReplacementDirect(molecule, source, target):
    for match in re.finditer(source, molecule):
        mBefore = molecule[0 : match.start()]
        mAfter = molecule[match.end() : ]
        yield "".join([mBefore, target, mAfter])


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        replacements = []
        molecule = ""
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                replacements.append(Replacement(*match.group(1, 2)))
            else:
                molecule += line
        return replacements, molecule.strip()
