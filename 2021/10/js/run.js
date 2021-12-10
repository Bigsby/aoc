"use strict";
const fs = require("fs")
const readline = require("readline")

const MATCHES = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

const ILLEGAL_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

const CLOSING_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

function solve(lines) {
    let illegalPoints = 0
    let incompletePoints = [] 
    for (const line of lines) {
        let expectedClosing = []
        let illegal = false
        for (let index = 0; index < line.length; index++) {
            const c = line[index]
            if (c == '(' || c == '[' || c == '{' || c == '<')
                expectedClosing.push(MATCHES[c])
            else if (c != expectedClosing.pop())
            {
                illegal = true
                illegalPoints += ILLEGAL_POINTS[c]
                break
            }
        }
        if (!illegal)
        {
            let points = 0;
            while (expectedClosing.length)
                points = points * 5 + CLOSING_POINTS[expectedClosing.pop()]
            incompletePoints.push(points)
        }
    }
    incompletePoints.sort((a, b) => a -b)
    return [illegalPoints, incompletePoints[Math.floor(incompletePoints.length / 2)]]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let lines = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    for await (const line of rl)
        lines.push(line)
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
