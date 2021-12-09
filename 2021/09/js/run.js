"use strict";
const fs = require("fs")
const readline = require("readline")

function getNeighbors(maxX, maxY, x, y) {
    let neighbors = []
    if (x)
        neighbors.push({ x: x - 1, y })
    if (y)
        neighbors.push({ x, y: y - 1 })
    if (x < maxX - 1)
        neighbors.push({ x: x + 1, y })
    if (y < maxY - 1)
        neighbors.push({ x, y: y + 1 })
    return neighbors
}

function getPositionRisk(input, maxX, maxY, x, y) {
    const height = input[y][x]
    for (const neighbor of getNeighbors(maxX, maxY, x, y))
        if (input[neighbor.y][neighbor.x] <= height)
            return 0
    return height + 1
}

function encodePosition(maxX, x, y) {
    return x + y * maxX
}

function decodePosition(maxX, value) {
    return { x: value % maxX, y: Math.floor(value / maxX) }
}

function getBasinSize(input, maxX, maxY, x, y) {
    let visited = new Set()
    let toVisit = []
    toVisit.push(encodePosition(maxX, x, y))
    while (toVisit.length)
    {
        const current = toVisit.shift()
        if (visited.has(current))
            continue
        visited.add(current)
        const position = decodePosition(maxX, current)
        const currentHeight = input[position.y][position.x]
        for (const neighbor of getNeighbors(maxX, maxY, position.x, position.y))
        {
            const neighborHeight = input[neighbor.y][neighbor.x]
            const neighborEncoded = encodePosition(maxX, neighbor.x, neighbor.y)
            if (neighborHeight == 9 || neighborHeight <= currentHeight || visited.has(neighborEncoded))
                continue
            toVisit.push(neighborEncoded)
        }
    }
    return visited.size
}

function addToSizes(sizes, size) {
    for (let index = 0; index < 3; index++)
        if (size >= sizes[index])
        {
            const oldSize = sizes[index];
            sizes[index] = size;
            size = oldSize;
        }
}

function solve(puzzleInput) {
    const maxX = puzzleInput[0].length;
    const maxY = puzzleInput.length;
    let lowestSum = 0;
    let sizes = Array(3).fill(0)
    for (let y = 0; y < maxY; y++)
        for (let x = 0; x < maxX; x++)
        {
            const positionRisk = getPositionRisk(puzzleInput, maxX, maxY, x, y)
            if (positionRisk) {
                lowestSum += positionRisk
                addToSizes(sizes, getBasinSize(puzzleInput, maxX, maxY, x, y))
            }
        }
    return [ lowestSum, sizes[0] * sizes[1] * sizes[2] ]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    const rl = readline.createInterface({ input: fs.createReadStream(filePath)})
    let heightMap = []

    for await (const line of rl) {
        let row = []
        for (let index = 0; index < line.length; index++)
            row.push(parseInt(line[index]))
        heightMap.push(row)
    }
    return heightMap
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
    main() }
