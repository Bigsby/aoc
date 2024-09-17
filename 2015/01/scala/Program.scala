import scala.util.control.Breaks._

type Input = List[Int]
type Result = (Int, Int)

def part2(directions: Input): Int =
  var currentFloor = 0
  var result = -1
  breakable { 
    for index <- directions.indices do
      currentFloor += directions(index)
      if currentFloor == -1 then
        result = index + 1
        break
  }
  if result == -1 then
    throw new Exception("Did not go below 0!")
  result

def solve(directions: Input): Result =
  (directions.sum, part2(directions))

def getInput(filePath: String): Input =
  val text = scala.io.Source.fromFile(filePath).mkString
  val directions = for direction <- text yield direction match
    case '(' => 1
    case ')' => -1
    case _ => throw new Exception(s"Uknown direction $direction")
  directions.toList

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
