"use strict";
const fs = require("fs")
const readline = require("readline")

function getBitCount(wire) {
    let count = 0
    while (wire) {
        count += wire & 1
        wire >>= 1
    }
    return count
}

function part1(connections) {
    return connections.reduce((soFar, connection) => soFar + connection.displays.filter(display => { 
        switch(getBitCount(display)) {
            case 2:
            case 3:
            case 4:
            case 7:
                return true;
            default:
                return false;
        }
    }).length, 0)
}

function findAndRemove(connection, digits, digit, digitLength, exceptDigit, exceptLength) {
    for (let wire = 0; wire < 10; wire++) {
        const segments = connection.wires[wire]
        if (!segments)
            continue
        const length = getBitCount(segments)
        if (length == digitLength && (!exceptLength || (getBitCount(segments & ~digits[exceptDigit]) == exceptLength))) {
            digits[digit] = segments
            connection.wires[wire] = 0
            return
        }
    }
}

function getConnectionValue(connection) {
    let digits = Array(10).fill(0)
    findAndRemove(connection, digits, 7, 3, 0, 0);
    findAndRemove(connection, digits, 4, 4, 0, 0);
    findAndRemove(connection, digits, 1, 2, 0, 0);
    findAndRemove(connection, digits, 8, 7, 0, 0);
    findAndRemove(connection, digits, 3, 5, 1, 3);
    findAndRemove(connection, digits, 6, 6, 1, 5);
    findAndRemove(connection, digits, 2, 5, 4, 3);
    findAndRemove(connection, digits, 5, 5, 4, 2);
    findAndRemove(connection, digits, 0, 6, 4, 3);
    for (const wire of connection.wires)
        if (wire) {
            digits[9] = wire
            break
        }
    let total = 0
    for (let display = 0; display < 4; display++)
        for (let digit = 0; digit < 10; digit++)
            if (connection.displays[display] == digits[digit])
                total += digit * (Math.pow(10, 3 - display))
    return total
}

function part2(connections) {
    return connections.reduce((soFar, connection) => soFar + getConnectionValue(connection), 0)
}

function solve(connections) {
    return [part1(connections), part2(connections)]
}

const A = "a".charCodeAt(0)
function parseSegments(segments) {
    let total = 0;
    for (let index = 0; index < segments.length; index++)
        total |= 1 << (segments.charCodeAt(index) - A)
    return total
}

async function getInput(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error("File not found")
    }
    const rl = readline.createInterface({ input: fs.createReadStream(filePath) })
    let connections = []
    for await (const line of rl)
    {
        const split = line.split(" | ")
        connections.push({
            wires: split[0].split(" ").map(parseSegments),
            displays: split[1].split(" ").map(parseSegments),
        })
    }
    return connections
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
