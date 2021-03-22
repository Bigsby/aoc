using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Program
    {
        static (int elf1, int elf2) ImproveRecipes(List<byte> recipes, int elf1, int elf2)
        {
            var elf1Score = recipes[elf1];
            var elf2Score = recipes[elf2];
            recipes.AddRange((elf1Score + elf2Score).ToString().Select(c => byte.Parse(c.ToString())));
            elf1 = (elf1 + elf1Score + 1) % recipes.Count;
            elf2 = (elf2 + elf2Score + 1) % recipes.Count;
            return (elf1, elf2);
        }

        static bool DoSequencesMatch(int start, IEnumerable<byte> recipes, int[] score)
        {
            if (start < 0)
                return false;
            for (var index = 0; index < score.Length; index++)
                if (recipes.ElementAt(index + start) != score[index])
                    return false;
            return true;
        }

        static (string, int) Solve(int target)
        {
            var scoreSequence = target.ToString().Select(c => int.Parse(c.ToString())).ToArray();
            var sequenceLength = scoreSequence.Length;
            var recipes = new List<byte> { 3, 7 };
            var elf1 = 0;
            var elf2 = 1;
            var index = 0;
            var part1Result = "";
            while (true)
            {
                (elf1, elf2) = ImproveRecipes(recipes, elf1, elf2);
                index = recipes.Count - sequenceLength - 1;
                if (string.IsNullOrEmpty(part1Result) && recipes.Count > target + 10)
                    part1Result = string.Join("", recipes.Skip(target).Take(10).Select(i => i.ToString()));
                if (DoSequencesMatch(index, recipes, scoreSequence))
                    return (part1Result, index);
                index++;
                if (DoSequencesMatch(index, recipes, scoreSequence))
                    return (part1Result, index);
            }
        }

        static int GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : int.Parse(File.ReadAllText(filePath).Trim());

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