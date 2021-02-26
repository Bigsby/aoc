using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    using Limits = Tuple<int, int>;
    class Program
    {
        static bool IsValidPassword(string password, bool check2)
        {
            if (string.Join("", password.OrderBy(c => c)) == password)
            {
                var counts = password.Distinct().ToDictionary(c => c, c => password.Count(t => t == c)).Values;
                return counts.Any(count => count > 1) && (!check2 || counts.Contains(2));
            }
            return false;
        }

        static int GetValidPasswordCount(Limits limits, bool check2)
        {
            var (start, end) = limits;
            return Enumerable.Range(start, end - start).Count(password => IsValidPassword(password.ToString(), check2));
        }

        static (int, int) Solve(Limits limits)
            => (
                GetValidPasswordCount(limits, false),
                GetValidPasswordCount(limits, true)
            );

        static Limits GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var split = File.ReadAllText(filePath).Trim().Split('-');
            return Tuple.Create(int.Parse(split[0]), int.Parse(split[1]));
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