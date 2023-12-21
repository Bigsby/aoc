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
        static int Part1(Input puzzleInput)
        { 
            var (times, distances) = puzzleInput;
            var count = times.Count();
            var result = 1;
            for (var index = 0; index < count; index++)
            {
                var (time, distance) = (times.ElementAt(index), distances.ElementAt(index));
                var winningWays = 0;
                for (var press = 1; press <= time / 2; press++)
                {
                    var testDistance = (time - press) * press;
                    if (testDistance > distance)
                        winningWays++;
                }
                result *= (winningWays * 2) - (time % 2 == 1 ? 0 : 1);
            }
            return result;
        }

        static BigInteger Part2(Input puzzleInput)
        {
            var (times, distances) = puzzleInput;
            var time = BigInteger.Parse(string.Join("", times.Select(t => t.ToString())));
            var distance = BigInteger.Parse(string.Join("", distances.Select(t => t.ToString())));
            Console.WriteLine($"{time}, {distance}");
            BigInteger middle = time / 2;
            var current = middle;
            BigInteger min = 0;
            BigInteger max = current;

            while (true) {
                var testDistance = (time  - current) * current;
                // Console.WriteLine($"{distance} = {testDistance} {max} {current} {min}"); Console.ReadLine();
                if (testDistance > distance)
                {
                    max = current;
                    current -= (current - min) / 2;
                }
                else if (testDistance < distance)
                {
                    min = current;
                    current = min + (max - min) / 2;
                    // Console.WriteLine($"top {top} bottom {bottom}");
                }
                if (current == max || current == min)
                {
                    Console.WriteLine($"{current} {time - current} ... {min} {max}");
                    return time - (current * 2) - (time % 2 == 1 ? 0 : 1) * 2 - (max - min);
                }
            }
        }

        static (int, BigInteger) Solve(Input puzzleInput)
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
