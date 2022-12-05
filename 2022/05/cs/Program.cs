using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = Tuple<Dictionary<int, List<char>>, List<Tuple<int, int, int>>>;

    static class Program
    {
        static Dictionary<int, List<char>> CopyStacks(Dictionary<int, List<char>> stacks)
        {
            var newStacks = new Dictionary<int, List<char>>();
            foreach (var (index, stack) in stacks)
                newStacks[index] = new List<char>(stacks[index]);
            return newStacks;
        }

        static string DoMoves(Input puzzleInput, bool moveMultipleCrates)
        {
            var (stacks, moves) = puzzleInput;
            stacks = CopyStacks(stacks);
            foreach (var (amount, source, target) in moves)
            {
                for (var targetIndex = 0; targetIndex < amount; targetIndex++)
                {
                    stacks[target].Insert(moveMultipleCrates ? targetIndex : 0, stacks[source][0]);
                    stacks[source].RemoveAt(0);
                }
            }
            var message = "";
            for (var index = 0; index < stacks.Count; index++)
                message += stacks[index + 1][0];
            return message;
        }

        static (string, string) Solve(Input puzzleInput)
        => (DoMoves(puzzleInput, false), DoMoves(puzzleInput, true));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var processingStacks = true;
            var stacks = new Dictionary<int, List<char>>();
            var moves = new List<Tuple<int, int, int>>();
            foreach (var line in File.ReadAllLines(filePath))
                if (processingStacks)
                {
                    if (line[1] == '1')
                        processingStacks = false;
                    else
                        foreach (var (crate, index) in line.Select((character, index) => (character, index)))
                            if (crate >= 'A' && crate <= 'Z')
                            {
                                var stackIndex = ((index - 1) / 4) + 1;
                                List<char> stack;
                                if (!stacks.TryGetValue(stackIndex, out stack))
                                    stack = stacks[stackIndex] = new List<char>();
                                stack.Add(crate);
                            }
                }
                else
                {
                    if (string.IsNullOrEmpty(line)) continue;
                    var splits = line.Split(" ");
                    moves.Add(Tuple.Create(int.Parse(splits[1]), int.Parse(splits[3]), int.Parse(splits[5])));
                }
            return Tuple.Create(stacks, moves);
        }

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
