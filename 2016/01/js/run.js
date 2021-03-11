"use strict";
const fs = require("fs");

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
            real = Number(operand)
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

    getManhatanDistance() {
        return Math.abs(this.real) + Math.abs(this.imag)
    }
}

class Instruction {
    constructor(direction, distance) {
        this.direction = direction
        this.distance = distance
    }
}

function getNewHeading(heading, direction) {
    return heading.multiply(direction === 'L' ? Complex.i : Complex.ni)
}

function solve(instructions) {
    let position = new Complex(0, 0)
    let heading = new Complex(0, 1)
    let part2 = 0
    let visited = []
    for (const instruction of instructions) {
        heading = getNewHeading(heading, instruction.direction)
        for (const _ of new Array(instruction.distance)) {
            position = position.add(heading)
            if (part2 === 0) {
                if (visited.find(v => position.equals(v)))
                    part2 = position.getManhatanDistance()
                else
                    visited.push(position)
            }
        }
    }
    return [position.getManhatanDistance(), part2]
}

function getInput(filePath) {
    if (!fs.existsSync(filePath))
        throw new Error("File not found")

    return Array.from(fs.readFileSync(filePath).toString().matchAll(/([RL])(\d+),?\s?/g))
        .map(match => new Instruction(match[1], parseInt(match[2])));
}

function main() {
    if (process.argv.length !== 3)
        throw new Error("Please, add input file path as parameter")

    let start = process.hrtime()
    let [part1Result, part2Result] = solve(getInput(process.argv[2]))
    const end = process.hrtime(start)
    console.log(`P1: ${part1Result}`)
    console.log(`P2: ${part2Result}`)
    console.log()
    console.log(`Time: ${((end[0] * 1e9 + end[1]) / 1e9).toFixed(7)}`)
}

if (require.main === module) {
    main()
}