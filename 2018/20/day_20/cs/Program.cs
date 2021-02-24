using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    class DefaultDictionary<TKey, TValue>
    {
        public DefaultDictionary(Func<TValue> generator) => _generator = generator;

        public TValue this[TKey key]
        {
            get
            {
                if (!_innerDictionary.ContainsKey(key))
                    _innerDictionary[key] = _generator();
                return _innerDictionary[key];
            }
            set => _innerDictionary[key] = value;
        }

        public IEnumerable<TValue> Values => _innerDictionary.Values;

        private IDictionary<TKey, TValue> _innerDictionary = new Dictionary<TKey, TValue>();
        private Func<TValue> _generator;
    }

    static class Program
    {
        static Dictionary<char, Complex> DIRECTIONS = new Dictionary<char, Complex> {
            { 'N', Complex.ImaginaryOne },
            { 'S', -Complex.ImaginaryOne },
            { 'E', 1 },
            { 'W', -1 }
        };

        static IEnumerable<int> GetDistances(string routes)
        {
            var distances = new DefaultDictionary<Complex, int>(() => int.MaxValue);
            distances[0] = 0;
            var groupEnds = new Stack<Complex>();
            var head = Complex.Zero;
            foreach (var c in routes[1..^1])
                switch (c)
                {
                    case '(': groupEnds.Push(head); break;
                    case ')': head = groupEnds.Pop(); break;
                    case '|': head = groupEnds.Peek(); break;
                    default:
                        var previous = head;
                        head += DIRECTIONS[c];
                        distances[head] = Math.Min(distances[head], distances[previous] + 1);
                        break;
                }
            return distances.Values;
        }

        static int Part1(string routes) => GetDistances(routes).Max();

        static int Part2(string routes) => GetDistances(routes).Where(distance => distance >= 1000).Count();

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
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
