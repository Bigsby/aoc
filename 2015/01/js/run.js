"use strict";
const fs = require("fs");

function part2(directions) {
    let currentFloor = 0
    for (let index = 0; index < directions.length; index++) {
        currentFloor += directions[index]
        if (currentFloor == -1)
            return index + 1
    }
}

function solve(directions) {
    return [directions.reduce((acc, direction) => acc + direction), part2(directions)]
}


function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    return fs.readFileSync(filePath).toString().trim().split("").map(c => c === "(" ? 1 : -1);
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

main()