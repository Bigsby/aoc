using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Collections.Generic;

namespace AoC
{
    using Input = Tuple<IEnumerable<int>, IEnumerable<int>>;

    static class Program
    {
        static BigInteger GetWinningWaysCount(BigInteger time, BigInteger distance)
        {
            BigInteger middle = time / 2;
            var current = middle;
            BigInteger min = 0;
            BigInteger max = current;

            while (true)
            {
                var testDistance = (time - current) * current;
                if (testDistance > distance)
                {
                    max = current;
                    current -= (current - min) / 2;
                }
                else if (testDistance < distance)
                {
                    min = current;
                    current = min + (max - min) / 2;
                }
                if (current == max || current == min || testDistance == distance)
                {
                    if (testDistance == distance)
                        current += 1;
                    if (testDistance > distance && time % 2 == 1)
                        current -= 1;
                    var result = time - (current * 2) + (time % 2 == 1 ? -1 : 1);
                    return time - (current * 2) + (time % 2 == 1 ? -1 : 1);
                }
            }
        }

        static BigInteger Part1(Input puzzleInput)
        {
            var (times, distances) = puzzleInput;
            return Enumerable.Range(0, times.Count())
                .Aggregate(new BigInteger(1), (soFar, index) => soFar * GetWinningWaysCount(times.ElementAt(index), distances.ElementAt(index)));
        }

        static BigInteger IntsToBigInteger(IEnumerable<int> values)
            => BigInteger.Parse(string.Join("", values.Select(v => v.ToString())));

        static BigInteger Part2(Input puzzleInput)
        {
            var (times, distances) = puzzleInput;
            return GetWinningWaysCount(IntsToBigInteger(times), IntsToBigInteger(distances));
        }

        static (BigInteger, BigInteger) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static IEnumerable<int> GetValues(string line)
            => line.Split(':')[1].Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(int.Parse);

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath))
                throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return Tuple.Create(GetValues(lines[0]), GetValues(lines[1]));
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
