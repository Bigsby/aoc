"use strict";
const fs = require("fs")
const readline = require("readline")

function getNeighbors(x, y)
{
    let neighbors = []
    if (x)
    {
        neighbors.push([ x - 1, y ])
        if (y)
            neighbors.push([ x - 1, y - 1 ])
        if (y < 9)
            neighbors.push([ x - 1, y + 1 ])
    }
    if (x < 9)
    {
        neighbors.push([ x + 1, y ])
        if (y)
            neighbors.push([ x + 1, y - 1 ])
        if (y < 9)
            neighbors.push([ x + 1, y + 1 ])
    }
    if (y)
        neighbors.push([ x, y - 1 ])
    if (y < 9)
        neighbors.push([ x, y + 1 ])
    return neighbors
}

function solve(octopuses) {
    let flashes = 0
    let allFlashes = 0
    let step = 0
    while (!allFlashes || step <= 100)
    {
        step++;
        let stepFlashes = 0
        let toProcess = []
        for (let y = 0; y < 10; y++)
            for (let x = 0; x < 10; x++)
            {
                octopuses[y][x]++
                if (octopuses[y][x] == 10)
                    toProcess.push([x, y])
            }
        while (toProcess.length)
        {
            const [ x, y ] = toProcess.pop()
            if (octopuses[y][x] == 0)
                continue
            stepFlashes++
            octopuses[y][x] = 0
            for (const neighbor of getNeighbors(x, y))
            {
                const [neighborX, neighborY] = neighbor;
                if (octopuses[neighborY][neighborX] == 0)
                    continue
                octopuses[neighborY][neighborX]++
            if (octopuses[neighborY][neighborX] == 10)
                toProcess.push([ neighborX, neighborY ])
            }
        }
        if (step <= 100)
            flashes += stepFlashes
        if (stepFlashes == 100)
            allFlashes = step
    }
    return [flashes, allFlashes]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let octopuses = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    for await (const line of rl)
    {
        let row = []
        for (let index = 0; index < line.length; index++)
            row.push(parseInt(line[index]))
        octopuses.push(row)
    }
    return octopuses
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
