import java.io.File

typealias Input = List<Int>
typealias Result = Pair<Int, Int>

fun part2(directions: Input): Int {
    var currentFloor = 0
    for ((index, direction) in directions.withIndex()) {
        currentFloor += direction
        if (currentFloor == -1)
            return index + 1
    }
    throw Exception("Did not go below 0!")
}

fun solve(directions: Input): Result {
    return Pair(directions.sum(), part2(directions))
}

fun getInput(filePath: String): Input {
    return File(filePath).readText().map { 
        when (it) {
            '(' -> 1
            ')' -> -1
            else -> throw Exception("Unknow direction $it")
        }
    }
}

fun main(args: Array<String>) {
    require(args.size  == 1) { "Please, add input file path as parameter." }
    val input = getInput(args[0])
    val start = System.nanoTime()
    val (part1, part2) = solve(input)
    val end = System.nanoTime()
    println("Part1: $part1")
    println("Part2: $part2")
    println("\nTime: %.7f".format((end - start) * 1e-9))
}
