"use strict";
const fs = require("fs")
const readline = require("readline")

function findPaths(edges, repeat) {
    let completePathCount = 0
    let queue = [ ["start", "start", !repeat ] ]
    while (queue.length)
    {
        const [ node, path, smallRepeat ] = queue.shift()
        if (node == "end")
            completePathCount++
        else
            for (const edge of edges.filter(edge => edge[0] == node || edge[1] == node))
            {
                const other = edge[0] == node ? edge[1] : edge[0]
                const smallIncluded = other == other.toLowerCase() && path.includes(other)
                if (!(other == "start" || (smallRepeat && smallIncluded)))
                    queue.push([ other, `${path},${other}`, smallRepeat || smallIncluded ])
            }
    }
    return completePathCount
}

function solve(edges) {
    return [findPaths(edges, false), findPaths(edges, true)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let edges = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    for await (const line of rl)
    {
        let split = line.split("-")
        edges.push([ split[0], split[1] ])
    }


    return edges
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
