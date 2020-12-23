import sys, os

def runProgram(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb

    pointer = 0

    while memory[pointer] != 99:
        instruction = memory[pointer]
        operand1 = memory[pointer + 1]
        operand2 = memory[pointer + 2]
        output = memory[pointer + 3]

        if instruction == 1:
            memory[output] = memory[operand1] + memory[operand2]
        elif instruction == 2:
            memory[output] = memory[operand1] * memory[operand2]
        else:
            raise Exception(f"Unknown instruction at {pointer}: {instruction}")

        pointer += 4
        
    return memory[0]

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        contents = file.read().strip()
        return map(int, contents.split(","))
