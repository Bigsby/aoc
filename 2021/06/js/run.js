"use strict";
const fs = require("fs");

function runGenerations(fishes, generations) {
    let fishCounts = Array(9).fill(0)
    for (const fish of fishes)
        fishCounts[fish]++
    while (generations--) {
        const fishesAtZero = fishCounts[0]
        for (let day = 0; day < 8; day++)
            fishCounts[day] = fishCounts[day + 1]
        fishCounts[8] = fishesAtZero
        fishCounts[6] += fishesAtZero
    }
    return fishCounts.reduce((soFar, count) => soFar + count)
}

function solve(puzzleInput) {
    return [runGenerations(puzzleInput, 80), runGenerations(puzzleInput, 256)]
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
