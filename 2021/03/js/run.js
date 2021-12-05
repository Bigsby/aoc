"use strict";
const fs = require("fs")
const readline = require("readline")

function getNthBitOnesCount(numbers, index) {
    const mask = 1 << index
    return numbers.filter(number => (number & mask) == mask).length
}

function processBit(numbers, index, mostCommon) {
    if (numbers.length == 1)
        return numbers
    const onesCount = getNthBitOnesCount(numbers, index)
    const zerosCount = numbers.length - onesCount
    const mask = 1 << index
    const match = mostCommon ^ (onesCount < zerosCount) ? mask : 0
    return numbers.filter(number => (number & mask) == match)
}

function part2(puzzleInput) {
    const [ bitLength, numbers ] = puzzleInput
    let oxygen = [...numbers]
    let co2 = [...numbers]
    let index = bitLength - 1
    while (oxygen.length > 1 || co2.length > 1)
    {
        oxygen = processBit(oxygen, index, true)
        co2 = processBit(co2, index, false)
        index--
    }
    return oxygen[0] * co2[0]
}

function part1(puzzleInput) {
    const [ bitLength, numbers ] = puzzleInput
    let gamma = 0
    let epsilon = 0
    const half = numbers.length / 2
    for (let index = bitLength - 1; index >= 0; index--)
    {
        const onesCount = getNthBitOnesCount(numbers, index)
        gamma = (gamma << 1) + (onesCount > half)
        epsilon = (epsilon << 1) + (onesCount < half)
    }
    return gamma * epsilon
}

function solve(puzzleInput) {
    return [part1(puzzleInput), part2(puzzleInput)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let bitLength = 0
    let numbers = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) });
    for await (const line of rl)
    {
        if (!bitLength)
            bitLength = line.length
        numbers.push(parseInt(line, 2))
    }
    return [ bitLength, numbers ]
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
