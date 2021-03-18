#! /opt/swift/usr/bin/swift

import Foundation

func part1(_ puzzleInput: String) -> Int {
    1
}

func part2(_ puzzleInput: String) -> Int {
    2
}

func solve(_ puzzleInput: String) -> (Int, Int) {
    (part1(puzzleInput), part2(puzzleInput))
}

func getInput(_ filePath: String) throws -> String {
    do {
        let contents = try String(
            contentsOf: URL.init(fileURLWithPath: filePath), 
            encoding: .utf8)
        let _ = contents.components(separatedBy: .newlines)
        
        return contents
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