using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using State = IEnumerable<long>;
    using Notes = Dictionary<long, bool>;

    class Program
    {
        
        static long GetStateValue(long index, State state)
            => (long)Enumerable.Range(0, 5).Sum(i => state.Contains(i + index - 2) ? Math.Pow(2, i) : 0);

        static IEnumerable<long> RunGenerations(Tuple<State, Notes> puzzleInput, int generations)
        {
            var (state, notes) = puzzleInput;
            var generation = 0;
            while (generation < generations)
            {
                var minState = state.Min();
                var newState = new List<long>();

                for (var index = minState - 2; index < state.Max() + 2; index++)
                    if (notes[GetStateValue(index, state)])
                        newState.Add(index);
                state = newState;
                generation++;
            }
            return state;
        }

        static long Part1(Tuple<State, Notes> puzzleInput)
            => RunGenerations(puzzleInput, 20).Sum();

        static long Part2(Tuple<State, Notes> puzzleInput)
        {
            var jump = 200;
            var firstState = RunGenerations(puzzleInput, jump);
            var firstSum = firstState.Sum();
            var secondState = RunGenerations(Tuple.Create(firstState, puzzleInput.Item2), jump);
            var diff = secondState.Sum() - firstSum;
            long target = 5 * (long)(Math.Pow(10, 10));
            return firstSum + diff * (target / jump - 1);
        }

        static Regex initialStateRegex = new Regex(@"#|\.", RegexOptions.Compiled);
        static IEnumerable<long> ParseInitialState(string line)
        {
            return initialStateRegex.Matches(line).Select((match, index) => (match.Groups[0].Value, index))
                .Where(pair => pair.Value == "#")
                .Select(pair => (long)pair.index);
        }

        static long ComputePattern(string pattern)
            => (long)pattern.Select((c, index) => (c, index)).Sum(pair => pair.c == '#' ? Math.Pow(2, pair.index) : 0);
        
        static Regex notesRegex = new Regex(@"^(?<pattern>[#\.]{5})\s=>\s(?<result>[#\.])$", RegexOptions.Compiled | RegexOptions.Multiline);
        static Notes ParseNotes(string noteLines)
            => noteLines.Split(Environment.NewLine).Select(line => notesRegex.Match(line))
                .ToDictionary(
                    match => ComputePattern(match.Groups["pattern"].Value), 
                    match => match.Groups["result"].Value == "#");

        static Tuple<State, Notes> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var split = File.ReadAllText(filePath).Split("\n\n");
            return Tuple.Create(ParseInitialState(split[0]), ParseNotes(split[1]));
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var part1Result = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            var part2Result = Part2(puzzleInput);
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}