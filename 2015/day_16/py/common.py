import sys, os, re


lineRegex = re.compile(r"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$")


props = [ "children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes" ]


def buildPropDict():
    return { prop: "N/A" for prop in props }
    

class AuntRecord():
    def __init__(self, number, prop1Name, prop1Value, prop2Name, prop2Value, prop3Name, prop3Value):
        self.number = int(number)
        self.props = buildPropDict()
        self.setProp(prop1Name, prop1Value)
        self.setProp(prop2Name, prop2Value)
        self.setProp(prop3Name, prop3Value)

    def setProp(self, name, value):
        self.props[name] = int(value)

    def __str__(self):
        return f"{self.number} => {self.props}"
    def __repr__(self):
        return self.__str__()


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
            match = lineRegex.match(line)
            if match:
                yield AuntRecord(*match.group(1, 2, 3, 4, 5, 6, 7))
