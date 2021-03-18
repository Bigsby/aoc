#! /opt/swift/usr/bin/swift

import Foundation

func part2(_ directions: [Int]) throws -> Int {
    var currentFloor = 0
    for (index, direction) in directions.enumerated() {
        currentFloor += direction
        if currentFloor == -1 {
            return index + 1
        }
    }
    throw "Did not get below 0"
}

func solve(_ puzzleInput: [Int]) -> (Int, Int) {
    (puzzleInput.reduce(0, +), try! part2(puzzleInput))
}

func getInput(_ filePath: String) throws -> [Int] {
    do {
        let contents = try String(
            contentsOf: URL.init(fileURLWithPath: filePath), 
            encoding: .utf8)

        return contents.map { c in c == "(" ? 1 : -1 }
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