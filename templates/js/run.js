"use strict";
const fs = require("fs");

function part2(puzzleInput) {
    return puzzleInput.length
}

function part1(puzzleInput) {
    return puzzleInput.length
}

function solve(puzzleInput) {
    return [part1(puzzleInput), part2(puzzleInput)]
}

function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    return fs.readFileSync(filePath).toString().trim()
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