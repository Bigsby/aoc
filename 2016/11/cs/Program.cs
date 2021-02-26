using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Floor = List<int>;
    record Elevator(int partA, int partB);
    record Move(int currentFloor, int nextFloor, Elevator elevator);
    record State(int currentFloor, Floor[] floors);
    
    class Program
    {
        const int EMPTY_SLOT = 0;
        static Dictionary<string, int> radioisotopes = new Dictionary<string, int>();

        static bool IsGroupValid(IEnumerable<int> group)
        {
            var testGroup = group.ToList();
            var generators = group.Where(part => part > 0);
            foreach (var generator in generators)
                if (testGroup.Contains(-generator))
                {
                    testGroup.Remove(-generator);
                    testGroup.Remove(generator);
                }
            return !testGroup.Any() || (testGroup.Any(part => part > 0) ^ testGroup.Any(part => part < 0));
        }

        static bool IsMoveValid(Floor currentFloor, Floor nextFloor, Elevator elevator)
        {
            var currentTestFloor = currentFloor.ToList();
            currentTestFloor.Remove(elevator.partA);
            currentTestFloor.Remove(elevator.partB);
            var nextTestFloor = nextFloor.ToList();
            if (elevator.partA != EMPTY_SLOT)
                nextTestFloor.Add(elevator.partA);
            if (elevator.partB != EMPTY_SLOT)
                nextTestFloor.Add(elevator.partB);
            return IsGroupValid(currentTestFloor) && IsGroupValid(nextTestFloor);
        }

        static State MakeMove(IEnumerable<Floor> floors, Move move)
        {
            var nextFloors = floors.Select(floor => floor.ToList()).ToArray();
            if (move.elevator.partA != EMPTY_SLOT)
            {
                nextFloors[move.currentFloor].Remove(move.elevator.partA);
                nextFloors[move.nextFloor].Add(move.elevator.partA);
            }
            if (move.elevator.partB != EMPTY_SLOT)
            {
                nextFloors[move.currentFloor].Remove(move.elevator.partB);
                nextFloors[move.nextFloor].Add(move.elevator.partB);
            }
            return new State(move.nextFloor, nextFloors);
        }

        static IEnumerable<Move> GetValidDirectionalMoves(State state, int direction, IEnumerable<Elevator> possibleMovesGroups)
        {
            var (currentFloor, floors) = state;
            var nextFloor = currentFloor + direction;
            var validMoves = new List<Move>();
            if ((nextFloor < 0 || nextFloor == floors.Length)
                || (nextFloor == 0 && floors[nextFloor].Count == 0)
                || (nextFloor == 1 && !(floors[1].Count > 0 || floors[0].Count > 0)))
                return validMoves;
            foreach (var move in possibleMovesGroups)
                if (IsMoveValid(floors[currentFloor], floors[nextFloor], move))
                    validMoves.Add(new Move(currentFloor, nextFloor, move));
            return validMoves;
        }

        static IEnumerable<Move> PruneMoves(List<Move> moves)
        {
            var pairMoves = moves.Where(move => move.elevator.partA == -move.elevator.partB).ToArray();
            if (pairMoves.Length > 1)
                foreach (var pairMove in pairMoves)
                    moves.Remove(pairMove);
            var upstairsMoves = moves.Where(move => move.currentFloor < move.nextFloor).ToArray();
            var singleUpMoves = upstairsMoves.Where(move => move.elevator.partA == EMPTY_SLOT || move.elevator.partB == EMPTY_SLOT).ToArray();
            if (singleUpMoves.Length != upstairsMoves.Length)
                foreach (var singleUpMove in singleUpMoves)
                    moves.Remove(singleUpMove);
            var downstairsMoves = moves.Where(move => move.currentFloor > move.nextFloor).ToArray();
            var pairDownstairsMoves = downstairsMoves.Where(move => move.elevator.partA != EMPTY_SLOT && move.elevator.partB != EMPTY_SLOT).ToArray();
            if (pairDownstairsMoves.Length != downstairsMoves.Length)
                foreach (var pairDownstairsMove in pairDownstairsMoves)
                    moves.Remove(pairDownstairsMove);
            return moves;
        }

        
        static IEnumerable<T[]> Combinations<T>(IEnumerable<T> source, int length)
        {
            T[] result = new T[length];
            Stack<int> stack = new Stack<int>();
            var data = source.ToArray();
            stack.Push(0);

            while (stack.Count > 0)
            {
                int resultIndex = stack.Count - 1;
                int dataIndex = stack.Pop();
                while (dataIndex < data.Length)
                {
                    result[resultIndex++] = data[dataIndex];
                    stack.Push(++dataIndex);
                    if (resultIndex == length)
                    {
                        yield return result;
                        break;
                    }
                }
            }
        }

        static IEnumerable<Move> GetValidMoves(State state)
        {
            var possibleMovesGroups = Combinations(state.floors[state.currentFloor].Concat(new [] { EMPTY_SLOT }), 2)
                .Where(IsGroupValid).Select(group => new Elevator(group.ElementAt(0), group.ElementAt(1)));
            var validMoves = GetValidDirectionalMoves(state, 1, possibleMovesGroups)
                .Concat(GetValidDirectionalMoves(state, -1, possibleMovesGroups)).ToList();
            return PruneMoves(validMoves);
        }

        static int SolveFloors(Floor[] floors)
        {
            var floorCount = floors.Length;
            var stack = new Stack<(State state, int movesCount)>();
            stack.Push((new State(0, floors), 0));
            while (stack.Any())
            {
                var (state, movesCount) = stack.Pop();
                foreach (var move in GetValidMoves(state))
                {
                    var newState = MakeMove(state.floors, move);
                    if (newState.currentFloor == floorCount - 1 && newState.floors[^1].Count == radioisotopes.Count * 2)
                        return movesCount + 1;
                    else
                        stack.Push((newState, movesCount + 1));
                    
                }
            }
            throw new Exception("Solution not found");
        }

        const string PART2_EXTRA = "a elerium generator, a elerium-compatible microchip, a dilithium generator, a dilithium-compatible microchip";
        static (int, int) Solve(Floor[] floors)
        {
            var part1Result = SolveFloors(floors);
            floors[0] = floors[0].Concat(ParseLine(PART2_EXTRA)).ToList();
            return (
                part1Result, 
                SolveFloors(floors)
            );
        }

        static Regex lineRegex = new Regex(@"a (?<radioisotope>\w+)(?<part>-compatible microchip| generator)", RegexOptions.Compiled);
        static Floor ParseLine(string line)
        {
            var result = new List<int>();
            foreach (Match match in lineRegex.Matches(line))
            {
                var radioisotope = match.Groups["radioisotope"].Value;
                if (radioisotopes.Count() == 0)
                    radioisotopes[radioisotope] = 1;
                else if (!radioisotopes.ContainsKey(radioisotope))
                    radioisotopes[radioisotope] = radioisotopes.Values.Max() + 1;
                var value = radioisotopes[radioisotope];
                result.Add(match.Groups["part"].Value.Contains("generator") ? value : -value);
            }
            return result;
        }

        static Floor[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(ParseLine).ToArray();

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var watch = Stopwatch.StartNew();
            var (part1Result, part2Result) = Solve(GetInput(args[0]));
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"Time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}