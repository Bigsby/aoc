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
        public bool Any() => _innerDictionary.Any();
        public IEnumerable<TKey> Keys => _innerDictionary.Keys;
        public IEnumerable<TValue> Values => _innerDictionary.Values; 

        public DefaultDictionary(Func<TValue> generator)
            => _generator = generator;

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

        public (TKey key, TValue value) Pop()
        {
            var result = _innerDictionary.First();
            _innerDictionary.Remove(result.Key);
            return (result.Key, result.Value);
        }

        public bool Remove(TKey key) => _innerDictionary.Remove(key);
        private Func<TValue> _generator;
        private Dictionary<TKey, TValue> _innerDictionary = new Dictionary<TKey, TValue>();
        public static implicit operator Dictionary<TKey, TValue>(DefaultDictionary<TKey, TValue> current)
            => current._innerDictionary;
    }

    static class Program
    {
        static Complex[] DIRECTIONS = new [] { 1, -1, Complex.ImaginaryOne, -Complex.ImaginaryOne };

        static bool GetsBug(bool hasBug, int adjacentCount)
            => hasBug ? adjacentCount == 1 : adjacentCount == 1 || adjacentCount == 2;

        static IEnumerable<Complex> NextMinute(IEnumerable<Complex> bugs)
        {
            var nextState = new List<Complex>();
            for (var y = 0; y < 5; y++)
                for (var x = 0; x < 5; x++)
                {
                    var position = new Complex(x, y);
                    var adjacentCount = DIRECTIONS.Count(direction => bugs.Contains(position + direction));
                    if (GetsBug(bugs.Contains(position), DIRECTIONS.Count(direction => bugs.Contains(position + direction))))
                        nextState.Add(position);
                }
            return nextState;
        }

        static bool Same<T>(IEnumerable<T> a, IEnumerable<T> b)
            => !a.Except(b).Any() && !b.Except(a).Any();

        static int Part1(IEnumerable<Complex> bugs)
        {
            var previous = new List<Complex[]> { bugs.ToArray() };
            while (true)
            {
                bugs = NextMinute(bugs);
                if (previous.Any(p => Same(p, bugs)))
                    break;
                previous.Add(bugs.ToArray());
            }
            var biodiversity = 0;
            for (var y = 0; y < 5; y++)
                for (var x = 0; x < 5; x++)
                    if (bugs.Contains(new Complex(x, y)))
                        biodiversity += 1 << (y * 5 + x);
            return biodiversity;
        }

        static Complex CENTER = new Complex(2, 2);
        static Complex MIDDLE_TOP = new Complex(2, 1);
        static Complex MIDDLE_LEFT = new Complex(1, 2);
        static Complex MIDDLE_RIGHT = new Complex(3, 2);
        static Complex MIDDLE_BOTTOM = new Complex(2, 3);
        static IEnumerable<int> CYCLE = Enumerable.Range(0, 5);
        static DefaultDictionary<int, List<Complex>> NextLayeredMinute(DefaultDictionary<int, List<Complex>> layers)
        {
            var newState = new DefaultDictionary<int, List<Complex>>(() => new List<Complex>());
            var lowerLayer = layers.Keys.Min() - 1;
            var upperLayer = layers.Keys.Max() + 2;
            for (var layer = lowerLayer; layer < upperLayer; layer++)
                for (var y = 0; y < 5; y++)
                    for (var x = 0; x < 5; x++)
                    {
                        var position = new Complex(x, y);
                        if (position == CENTER)
                            continue;
                        var adjacentCount = DIRECTIONS.Count(direction => layers[layer].Contains(position + direction));
                        if (y == 0 && layers[layer - 1].Contains(MIDDLE_TOP))
                            adjacentCount++;
                        else if (y == 4 && layers[layer - 1].Contains(MIDDLE_BOTTOM))
                            adjacentCount++;
                        
                        if (x == 0 && layers[layer - 1].Contains(MIDDLE_LEFT))
                            adjacentCount++;
                        else if (x == 4 && layers[layer - 1].Contains(MIDDLE_RIGHT))
                            adjacentCount++;
                        
                        if (position == MIDDLE_TOP)
                            adjacentCount += CYCLE.Count(x => layers[layer + 1].Contains(new Complex(x, 0)));
                        else if (position == MIDDLE_LEFT)
                            adjacentCount += CYCLE.Count(y => layers[layer + 1].Contains(new Complex(0, y)));
                        else if (position == MIDDLE_RIGHT)
                            adjacentCount += CYCLE.Count(y => layers[layer + 1].Contains(new Complex(4, y)));
                        else if (position == MIDDLE_BOTTOM)
                            adjacentCount += CYCLE.Count(x => layers[layer + 1].Contains(new Complex(x, 4)));
                        if (GetsBug(layers[layer].Contains(position), adjacentCount))
                            newState[layer].Add(position);
                    }
            return newState;
        }

        static int Part2(IEnumerable<Complex> bugs)
        {
            var layers = new DefaultDictionary<int, List<Complex>>(() => new List<Complex>());
            layers[0] = bugs.ToList();
            foreach (var _ in Enumerable.Range(0, 200))
                layers = NextLayeredMinute(layers);
            return layers.Values.Sum(bugs => bugs.Count);
        }

        static (int, int) Solve(IEnumerable<Complex> bugs)
            => (
                Part1(bugs),
                Part2(bugs)
            );

        static IEnumerable<Complex> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    if (c == '#')
                        yield return new Complex(x, y);
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
