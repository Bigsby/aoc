using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<(int, IEnumerable<int[]>)>;

    static class Program
    {
        static int[] MAX_BALLS = new [] { 12, 13, 14 };

        static bool IsGamePossible((int, IEnumerable<int[]>) game)
        {
            foreach (var draw in game.Item2)
                for (var index = 0; index < 3; index++)
                    if (draw[index] > MAX_BALLS[index])
                        return false;
            return true;
        }

        static int GetPowers((int, IEnumerable<int[]>) game)
        {
            var mins = new [] { 0, 0, 0 };
            foreach (var draw in game.Item2)
                for (var index = 0; index < 3; index++)
                    mins[index] = Math.Max(mins[index], draw[index]);
            return mins[0] * mins[1] * mins[2];
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Where(IsGamePossible).Sum(game => game.Item1), puzzleInput.Sum(GetPowers));
        
        static int[] ParseDraw(string text)
        {
            var colours = new Dictionary<string, int>
            {
                { "red", 0 },
                { "green", 0 },
                { "blue", 0 }
            };
            foreach ( var draw in text.Split(","))
            {
                var split = draw.Trim().Split(" ");
                colours[split[1]] = int.Parse(split[0]);
            }
            return new [] { colours["red"], colours["green"], colours["blue"] };
        }

        static (int, IEnumerable<int[]>) ParseGame(string line)
        {
            var separatorIndex = line.IndexOf(':');
            var (heading, drawsText) = (line[..separatorIndex], line[(separatorIndex + 2)..]);
            return (int.Parse(heading.Split(" ")[1]), drawsText.Split(";").Select(ParseDraw));
        }

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) 
                throw new FileNotFoundException(filePath);
            
            return File.ReadAllLines(filePath).Select(line => ParseGame(line.Trim()));
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
