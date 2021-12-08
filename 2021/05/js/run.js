"use strict";
const fs = require("fs")
const readline = require("readline")

function getCoveredPoints(lines, diagonals) {
    let diagram = new Map()
    const addToDiagram = (x, y) => {
        const key = `${x},${y}`
        diagram.set(key, diagram.has(key) ? diagram.get(key) + 1 : 1)
    }
    for (const line of lines) {
        const [x1, y1, x2, y2] = line
        if (x1 == x2)
            for (let y = y1 < y2 ? y1 : y2; y < (y1 > y2 ? y1 : y2) + 1; y++)
                addToDiagram(x1, y)
        else if (y1 == y2)
            for (let x = x1 < x2 ? x1 : x2; x < (x1 > x2 ? x1 : x2) + 1; x++)
                addToDiagram(x, y1)
        else if (diagonals) {
            const xDirection = x2 > x1 ? 1 : -1
            const yDirection = y2 > y1 ? 1 : -1
            const count = Math.abs(x2 - x1) + 1
            for (let xy = 0; xy < count; xy++)
                addToDiagram(x1 + xy * xDirection, y1 + xy * yDirection)
        }
    }
    let total = 0
    for (const [_, value] of diagram)
        if (value > 1)
            total++
    return total
}

function solve(puzzleInput) {
    return [getCoveredPoints(puzzleInput, false), getCoveredPoints(puzzleInput, true)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let lines = []
    const lineRegex = /(\d+),(\d+) -> (\d+),(\d+)/
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    for await (const line of rl) {
        const match = line.match(lineRegex)
        if (match)
            lines.push([
                parseInt(match[1]),
                parseInt(match[2]),
                parseInt(match[3]),
                parseInt(match[4])
            ])
        else
            throw new Error(`Bad line: ${line}`)
    }

    return lines
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
