#! /opt/swift/usr/bin/swift

import Foundation

typealias Instruction = (Character, Int)

struct Coordinate: Equatable {
    var x: Int
    var y: Int
    
    init(_ x: Int, _ y: Int ) {
        self.x = x
        self.y = y
    }

    var manhatanDistance: Int {
        abs(self.x) + abs(self.y)
    }

    static let i = Coordinate(0, 1)
}

extension Coordinate {
    static func + (a: Coordinate, b: Coordinate) -> Coordinate {
        Coordinate(a.x + b.x, a.y + b.y)
    }

    static func * (a: Coordinate, b: Coordinate) -> Coordinate {
        Coordinate(a.x * b.x - a.y * b.y, a.y * b.x + a.x * b.y)
    }

    static func * (a: Coordinate, b: Int) -> Coordinate {
        Coordinate(a.x * b, a.y * b)
    }

    static func += (a: inout Coordinate, b: Coordinate) {
        a = a + b
    }
}

func solve(_ instructions: [Instruction]) -> (Int, Int) {
    var position = Coordinate(0, 0)
    var heading = Coordinate(0, 1)
    var part2 = 0
    var visited: [Coordinate] = []
    for (direction, distance) in instructions {
        heading = heading * (direction == "L" ? 1 : -1) * Coordinate.i;
        for _ in 0..<distance {
            position += heading
            if part2 == 0 {
                if visited.contains(position) {
                    part2 = position.manhatanDistance
                } else {
                    visited.append(position)
                }
            }
        }
    }
    return (position.manhatanDistance, part2)
}

func getInput(_ filePath: String) throws -> [Instruction] {
    do {
        let contents = try String(
            contentsOf: URL.init(fileURLWithPath: filePath), encoding: .utf8)

        let instructionRegex = try! NSRegularExpression(pattern: #"(?<direction>[RL])(?<distance>\d+),?\s?"#, 
            options: [])
        return instructionRegex.matches(in: contents, options: [], range:NSMakeRange(0, contents.count))
            .map { match in
            (
                Array(contents.substring(with: match.range(withName: "direction")))[0], 
                Int(contents.substring(with: match.range(withName: "distance")))!
            )
        }
    }
    catch {
        throw "unable to read file"
    }
}

func main() throws {
    if CommandLine.arguments.count != 2 {
        throw "Please, add input file path as parameter"
    }
    let start = DispatchTime.now()
    let (part1Result, part2Result) = solve(try! getInput(CommandLine.arguments[1]))
    let ellapsed = DispatchTime.now().uptimeNanoseconds - start.uptimeNanoseconds
    print("P1: \(part1Result)")
    print("P2: \(part2Result)")
    print()
    print(String(format: "Time: %.07f", Double(ellapsed) * 1e-9))
}

extension String: Error {}
do {
    try main()
} catch let error as String {
    print(error)
}