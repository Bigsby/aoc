"use strict";
const fs = require("fs");

function getCount(numbers, indexOffset) {
    let count = 0
    for (let index = 0; index < numbers.length; index++)
        if (numbers[index] == numbers[(index + indexOffset) % numbers.length])
            count += numbers[index]
    return count
}

function solve(numbers) {
    return [
        getCount(numbers, numbers.length - 1),
        getCount(numbers, Math.floor(numbers.length / 2))
    ]
}

function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    return Array.from(fs.readFileSync(filePath).toString().trim())
        .map(c => parseInt(c))
}

function main() {
    if (process.argv.length !== 3)
        throw new Error("Please, add input file path as parameter")
    let start = process.hrtime()
    let [part1Result, part2Result] = solve(getInput(process.argv[2]))
    let end = process.hrtime(start)
    console.log(`P1: ${part1Result}`)
    console.log(`P2: ${part2Result}`)
    console.log()
    console.log(`Time: ${((end[0] * 1e9 + end[1]) / 1e9).toFixed(7)}`)
}

if (require.main === module) {
    main()
}