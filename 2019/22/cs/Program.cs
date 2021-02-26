using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    static class Program
    {
        const int NEW_STACK = 0;
        const int CUT = 1;
        const int INCREMENT = 2;

        static IEnumerable<int> DoShuffles(IEnumerable<int> cards, IEnumerable<(int, int)> shuffles)
        {
            var cardsArray = cards.ToArray();
            var cardsCount = cards.Count();
            var replacement = new int[cardsCount];
            foreach (var (shuffle, count) in shuffles)
            {
                switch (shuffle)
                {
                    case NEW_STACK:
                        cardsArray = cardsArray.Reverse().ToArray();
                        break;
                    case CUT:
                        cardsArray = cardsArray[Range.StartAt(new Index(Math.Abs(count), count < 0))].Concat(cardsArray[Range.EndAt(new Index(Math.Abs(count), count < 0))]).ToArray();
                        break;
                    case INCREMENT:
                        var cardsStack = new Stack<int>(cards);
                        for (var index = 0; index < cardsCount; index++)
                            replacement[(index * count) % cardsCount] = cardsArray[index];
                        cardsArray = replacement.ToArray();
                        break;
                }
            }
            return cardsArray;
        }

        static BigInteger InverModulo(BigInteger a, BigInteger n)
            => BigInteger.ModPow(a, n - 2, n);

        static BigInteger AbsoluteModulo(BigInteger a, BigInteger n) => ((a % n) + n) % n;

        const long CARDS2 = 119315717514047L;
        const long RUNS = 101741582076661L;
        const long POSITION2 = 2020;
        static BigInteger Part2(IEnumerable<(int, int)> shuffles)
        {
            int la = 0, lb = 0;
            long a = 1, b = 0;
            foreach (var (shuffle, count) in shuffles)
            {
                switch (shuffle)
                {
                    case NEW_STACK:
                        la = -1;
                        lb = -1;
                        break;
                    case CUT:
                        la = 1;
                        lb = -count;
                        break;
                    case INCREMENT:
                        la = count;
                        lb = 0;
                        break;
                }
                a = (long)AbsoluteModulo(la * a, CARDS2);
                b = (long)AbsoluteModulo(la * b + lb, CARDS2);
            }
            var Ma = System.Numerics.BigInteger.ModPow(a, RUNS, CARDS2);
            var Mb = AbsoluteModulo((b * (Ma - 1) * InverModulo(a - 1, CARDS2)), CARDS2);
            return AbsoluteModulo((POSITION2 - Mb) * InverModulo(Ma, CARDS2), CARDS2);
        }

        const int CARDS1 = 10007;
        const int POSITION1 = 2019;
        static (int, BigInteger) Solve(IEnumerable<(int, int)> shuffles)
            => (
                DoShuffles(Enumerable.Range(0, CARDS1), shuffles).ToList().IndexOf(POSITION1),
                Part2(shuffles)
            );

        static IEnumerable<(int, int)> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line =>
            {
                if (line.StartsWith("deal into"))
                    return (NEW_STACK, 0);
                if (line.StartsWith("cut"))
                    return (CUT, int.Parse(line.Split(" ")[1]));
                if (line.StartsWith("deal with"))
                    return (INCREMENT, int.Parse(line.Split(" ")[^1]));
                throw new Exception($"Bad format '{line}'");
            });
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
