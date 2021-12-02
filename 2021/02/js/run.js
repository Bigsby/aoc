"use strict";
const fs = require("fs");
const readline = require("readline")

class Complex {
    constructor(real, imag) {
        this.real = Number(real) || 0
        this.imag = Number(imag) || 0
    }
    static i = new Complex(0, 1)
    static ni = new Complex(0, -1)

    add(other) {
        let real, imag
        if (other instanceof Complex) {
            real = other.real
            imag = other.imag
        } else {
            real = Number(other)
            imag = 0
        }
        return new Complex(this.real + real, this.imag + imag)
    }

    multiply(other) {
        let real, imag
        if (other instanceof Complex) {
            real = other.real
            imag = other.imag
        } else {
            real = Number(other)
            imag = 0
        }
        return new Complex(this.real * real - this.imag * imag, this.real * imag + this.imag * real)
    }

    equals(other) {
        return other instanceof Complex && this.real === other.real && this.imag === other.imag
    }
}


function part2(commands) {
    const forward = new Complex(1, 0)
    let position = new Complex(0, 0)
    let aim = new Complex(0, 0)
    for (const command of commands)
        if (command.direction.equals(forward))
            position = position.add(aim.add(1).multiply(command.units))
        else
            aim = aim.add(command.direction.multiply(command.units))
    
    return position.real * position.imag
}

function part1(commands) {
    let position = commands.reduce((position, command) => position.add(command.direction.multiply(command.units)), new Complex(0, 0))
    return position.real * position.imag
}

function solve(puzzleInput) {
    return [part1(puzzleInput), part2(puzzleInput)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let commands = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    for await (const line of rl) {
        const split = line.split(' ')
        const units = parseInt(split[1])
        let direction = new Complex(0, 0)
        switch (split[0]) {
            case "forward": direction = new Complex(1, 0); break;
            case "down": direction = new Complex(0, 1); break;
            case "up": direction = new Complex(0, -1); break;
            default: throw new Exception(`Unknow command ${split[0]}`)
        }
        commands.push({direction, units})
    }
    
    return commands 
}

async function main() {
    if (process.argv.length !== 3)
        throw new Error("Please, add input file path as parameter")
    let start = process.hrtime()
    let [part1Result, part2Result] = solve(await getInput(process.argv[2]))
    let end = process.hrtime(start)
    console.log(`P1: ${part1Result}`)
    console.log(`P2: ${part2Result}`)
    console.log()
    console.log(`Time: ${((end[0] * 1e9 + end[1]) / 1e9).toFixed(7)}`)
}

if (require.main === module) {
    main()
}
