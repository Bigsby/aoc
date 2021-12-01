"use strict";
const fs = require("fs");
const readline = require("readline");

function part2(depths) {
    let increments = 0
    let lastDepth = Number.MAX_SAFE_INTEGER
    for (let index = 0; index < depths.length - 2; index++)
    {
        const depth = depths[index] + depths[index + 1] + depths[index + 2]
        if (depth > lastDepth)
            increments++
        lastDepth = depth
    }
    return increments
}

function part1(depths) {
    let increments = 0
    let lastDepth = Number.MAX_SAFE_INTEGER
    for (const depth of depths)
    {
        if (depth > lastDepth)
            increments++
        lastDepth = depth
    }
    return increments
}

function solve(puzzleInput) {
    return [part1(puzzleInput), part2(puzzleInput)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) });
    let depths = []
    for await (const line of rl)
        depths.push(parseInt(line))

    return depths
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
