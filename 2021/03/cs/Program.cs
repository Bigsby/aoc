using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record Input(int bitLength, IEnumerable<int> numbers);

    static class Program
    {
        static int GetNthBits1Count(IEnumerable<int> numbers, int index)
        {
            var mask = 1 << index;
            return numbers.Count(number => (number & mask) == mask);
        }

        static int Part1(Input puzzleInput)
        { 
            var gamma = 0;
            var epsilon = 0;
            var half = puzzleInput.numbers.Count() / 2;
            for (var index = puzzleInput.bitLength - 1; index >= 0; index--)
            {
                var onesCount = GetNthBits1Count(puzzleInput.numbers, index);
                gamma = (gamma << 1) + (onesCount > half ? 1 : 0);
                epsilon = (epsilon << 1) + (onesCount < half ? 1 : 0);
            }
            return gamma * epsilon;
        }

        static IEnumerable<int> ProcessBit(IEnumerable<int> numbers, int index, bool mostCommon)
        {
            if (numbers.Count() == 1)
                return numbers;
            var onesCount = GetNthBits1Count(numbers, index);
            var zerosCount = numbers.Count() - onesCount;
            var mask = 1 << index;
            var match = mostCommon ^ (onesCount < zerosCount) ? mask : 0;
            return numbers.Where(number => (number & mask) == match);
        }

        static int Part2(Input puzzleInput)
        {
            IEnumerable<int> oxygen = new List<int>(puzzleInput.numbers);
            IEnumerable<int> co2 = puzzleInput.numbers;
            var index = puzzleInput.bitLength - 1;
            while (oxygen.Count() > 1 || co2.Count() > 1)
            {
                oxygen = ProcessBit(oxygen, index, true);
                co2 = ProcessBit(co2, index, false);
                index--;
            }
            return oxygen.First() * co2.First();
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Input GetInput(string filePath)
        {
            
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return new (lines[0].Length, lines.Select(line => Convert.ToInt32(line, 2)));

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
