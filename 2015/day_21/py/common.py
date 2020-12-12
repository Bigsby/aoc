import sys, os, re

inputRegex = re.compile(r"^Hit Points: (?P<hit>\d+)\W+Damage: (?P<damage>\d+)\W+^Armor: (?P<armor>\d+)", flags=re.MULTILINE)


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        contents = file.read()
        print(contents)
        match = inputRegex.match(contents)
        if match:
            return match.group("hit"), match.group("damage"), match.group("armor")
        else:
            raise Exception("Bad format input")
