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

        static (int, int) Solve(string routes)
        {
            var distances = GetDistances(routes);
            return (
                distances.Max(),
                distances.Count(distance => distance >= 1000)
            );
        }

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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
