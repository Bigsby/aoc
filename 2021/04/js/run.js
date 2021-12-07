"use strict";
const fs = require("fs")
const readline = require("readline")

function copyCards(cards) {
    let result = []
    for (const card of cards) {
        let copy = []
        for (const row of card)
            copy.push([...row])
        result.push(copy)
    }
    return result
}

function isCardComplete(card) {
    for (let x = 0; x < 5; x++) {
        let xComplete = true;
        let yComplete = true;
        for (let y = 0; y < 5; y++) {
            xComplete &= card[x][y] < 0
            yComplete &= card[y][x] < 0
        }
        if (xComplete || yComplete)
            return true
    }
    return false
}

function getCardUnmarkedSum(card) {
    let total = 0
    for (const row of card)
        for (const number of row)
            if (number > 0)
                total += number
    return total
}

function playGame(puzzleInput, first) {
    let [ numbers, cards ] = puzzleInput;
    cards = copyCards(cards)
    for (const number of numbers) {
        let toRemove = []
        for (let card of cards)
            for (let row of card)
                if (row.includes(number)) {
                    row[row.indexOf(number)] = -1
                    if (isCardComplete(card)) {
                        if (first)
                            return getCardUnmarkedSum(card) * number
                        toRemove.push(card)
                    }
                }
        for (const card of toRemove) {
            cards.splice(cards.indexOf(card), 1)
            if (cards.length == 0)
                return getCardUnmarkedSum(card) * number
        }
    }
}

function solve(puzzleInput) {
    return [playGame(puzzleInput, true), playGame(puzzleInput, false)]
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    let numbers = []
    let cards = []
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    let firstLine = true;
    let cardRow = -2
    let card = []
    for await (const line of rl) {
        if (firstLine) {
            firstLine = false
            numbers = line.split(',').map(Number)
        } else {
            cardRow++
            if (cardRow == -1)
                continue
            card.push(line.split(' ').filter(i => i).map(Number))
            if (cardRow == 4) {
                cards.push(card)
                card = []
                cardRow = -2
            }
        }
    }
    return [ numbers, cards ]
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
