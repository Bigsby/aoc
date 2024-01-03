using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<(string, IEnumerable<int>)>;

    static class Program
    {
        static IEnumerable<int> GetOnesCounts(int value)
        {
            var stringValue = Convert.ToString(value, 2);
            var count = 0;
            for (var index = 0; index < stringValue.Length; index++)
            {
                if (stringValue[index] == '1')
                    count++;
                else if (count > 0)
                {
                    yield return count;
                    count = 0;
                }
            }
            if (count > 0)
                yield return count;
        }

        static int FindBinaryArrangements(string record, IEnumerable<int> counts)
        {
            var validCount = 0;
            var countsArray = counts.ToArray();
            var unknows = record.Count(c => c == '?');
            var unknownIndexes = Enumerable.Range(0, record.Length).Where(index => record[index] == '?').ToArray();
            var intValue = Enumerable.Range(0, record.Length).Sum(index => record[index] == '#' ? 1 << (record.Length - index - 1) : 0);
            for (var test = 0; test < 1 << unknows; test++)
            {
                var testValue = intValue;
                for (var unknowIndex = 0; unknowIndex < unknownIndexes.Length; unknowIndex++)
                    if (((test >> unknowIndex) & 1) == 1)
                        testValue += (1 << (record.Length - unknownIndexes[unknowIndex] - 1));
                validCount += GetOnesCounts(testValue).SequenceEqual(countsArray) ? 1 : 0;
            }
            return validCount;

        }
        
        static int FindArrangements(string record, IEnumerable<int> counts)
        {
            var validCount = 0;
            var countsArray = counts.ToArray();
            var unknows = record.Count(c => c == '?');
            var unknownIndexes = Enumerable.Range(0, record.Length).Where(index => record[index] == '?');
            var testValue = Enumerable.Range(0, record.Length).Sum(index => record[index] == '#' ? 1 << (record.Length - index - 1) : 0);
            // var binaryString = Convert.ToString(testValue, 2);
            
            // WriteLine($"{record} {string.Join(",", unknownIndexes.Select(i => i.ToString()))} {testValue} {binaryString}");
            for (var test = 0; test < 1 << unknows; test++)
            {
                var testRecord = record.ToCharArray();
                var unknowIndex = 0;
                for (var index = 0; index < testRecord.Length; index++)
                {
                    if (testRecord[index] == '?')
                        testRecord[index] = ((test >> unknowIndex++) & 1) == 1 ? '#' : '.';
                }
                var testString = new string(testRecord);
                var testGroups = testString.Split(".", StringSplitOptions.RemoveEmptyEntries);
                if (testGroups.Length != countsArray.Length)
                    continue;
                validCount += Enumerable.Range(0, testGroups.Length).All(index => testGroups[index].Length == countsArray[index]) ? 1 : 0;
            }
            return validCount;
        }

        static int Part2(Input puzzleInput)
        {
            return 2;
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Sum(row => FindBinaryArrangements(row.Item1, row.Item2)), Part2(puzzleInput));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => 
            {
                var split = line.Trim().Split(' ');
                return (split[0], split[1].Split(',').Select(int.Parse));
            });

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
