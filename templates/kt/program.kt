import java.io.File

typealias Input = String
typealias Result = Pair<Int, Int>

fun part1(input: Input): Int {
    return 1
}

fun part2(input: Input): Int {
    return 2
}

fun solve(input: Input): Result {
    return Pair(part1(input), part2(input))
}

fun getInput(filePath: String): Input {
    return File(filePath).readText()
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
