import scala.util.control.Breaks._

type Input = String
type Result = (Int, Int)

def part1(input: Input): Int =
  1

def part2(input: Input): Int =
  2

def solve(input: Input): Result =
  (part1(input), part2(input))

def getInput(filePath: String): Input =
  scala.io.Source.fromFile(filePath).mkString

def main(args: Array[String]) = 
  if args.size != 1 then
    throw new Exception("Please, add input file as parameter")
  val input = getInput(args(0))
  var start = System.nanoTime
  val (part1, part2) = solve(input)
  var end = System.nanoTime
  println(s"Part 1: $part1")
  println(s"Part 2: $part2")
  println(f"\nTime: ${(end - start) * 1e-9}%.7f")
