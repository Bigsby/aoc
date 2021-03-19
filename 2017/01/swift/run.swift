#! /opt/swift/usr/bin/swift

import Foundation

func getCount(_ numbers: [Int], _ indexOffset: Int) -> Int {
    var count = 0
    for index in 0..<numbers.count {
        if numbers[index] == numbers[(index + indexOffset) % numbers.count] {
            count += numbers[index]
        }
    }
    return count
}

func solve(_ numbers: [Int]) -> (Int, Int) {
    (getCount(numbers, numbers.count - 1), getCount(numbers, numbers.count / 2))
}

func getInput(_ filePath: String) throws -> [Int] {
    do {
        let contents = try String(
            contentsOf: URL.init(fileURLWithPath: filePath), 
            encoding: .utf8)
        
        return contents.trimmingCharacters(in: .whitespacesAndNewlines).map { c in c.wholeNumberValue! }
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