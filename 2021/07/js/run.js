"use strict";
const fs = require("fs");

function getDistanceCost(posA, posB) {
    const distance = Math.abs(posA - posB)
    return (distance * (distance + 1)) / 2
}
function part2(crabs) {
    const average = Math.floor(crabs.reduce((soFar, position) => soFar + position, 0) / crabs.length)
    return crabs.reduce((soFar, position) => soFar + getDistanceCost(average, position), 0)
}

function part1(crabs) {
    crabs.sort((a, b) => a - b)
    const mean = crabs[crabs.length / 2]
    return crabs.reduce((soFar, position) => soFar + Math.abs(position - mean), 0)
}

function solve(crabs) {
    return [part1(crabs), part2(crabs)]
}

function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    return fs.readFileSync(filePath).toString().trim().split(',').map(Number)
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
