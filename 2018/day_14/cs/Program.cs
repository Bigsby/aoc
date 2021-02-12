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
        static (int elf1, int elf2) ImproveRecipes(List<int> recipes, int elf1, int elf2)
        {
            var elf1Score = recipes[elf1];
            var elf2Score = recipes[elf2];
            recipes.AddRange((elf1Score + elf2Score).ToString().Select(c => int.Parse(c.ToString())));
            elf1 = (elf1 + elf1Score + 1) % recipes.Count;
            elf2 = (elf2 + elf2Score + 1) % recipes.Count;
            return (elf1, elf2);
        }

        static string Part1(int target)
        {
            var recipes = new List<int> { 3, 7 };
            var elf1 = 0;
            var elf2 = 1;
            while (recipes.Count < target + 10)
                (elf1, elf2) = ImproveRecipes(recipes, elf1, elf2);
            return string.Join("", recipes.Skip(target).Take(10).Select(i => i.ToString()));
        }

        static bool DoSequencesMatch(int start, IEnumerable<int> recipes, int[] score)
        {
            if (start < 0)
                return false;
            for (var index = 0; index < score.Length; index++)
                if (recipes.ElementAt(index + start) != score[index])
                    return false;
            return true;
        }

        static int Part2(int target)
        {
            var scoreSequence = target.ToString().Select(c => int.Parse(c.ToString())).ToArray();
            var sequenceLength = scoreSequence.Length;
            var recipes = new List<int> { 3, 7 };
            var elf1 = 0;
            var elf2 = 1;
            var index = 0;
            while (true)
            {
                (elf1, elf2) = ImproveRecipes(recipes, elf1, elf2);
                index = recipes.Count - sequenceLength - 1;
                if (DoSequencesMatch(index, recipes, scoreSequence))
                    return index;
                index++;
                if (DoSequencesMatch(index, recipes, scoreSequence))
                    return index;
            }
        }

        static int GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return int.Parse(File.ReadAllText(filePath).Trim());
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