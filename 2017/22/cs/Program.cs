using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using InfectionStatus = Dictionary<Complex, bool>;

    class DefaultDictionary<TKey, TValue>
    {
        public bool Any() => _innerDictionary.Any();
        public IEnumerable<TKey> Keys => _innerDictionary.Keys;

        public DefaultDictionary(Dictionary<TKey, TValue> init = default(Dictionary<TKey, TValue>))
            => _innerDictionary = init ?? new Dictionary<TKey, TValue>();

        public TValue this[TKey key]
        {
            get
            {
                if (!_innerDictionary.ContainsKey(key))
                    _innerDictionary[key] = default(TValue);
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

        private IDictionary<TKey, TValue> _innerDictionary;
    }

    static class Program
    {
        static int Part1(InfectionStatus initalState)
        {
            var state = new DefaultDictionary<Complex, bool>(new Dictionary<Complex, bool>(initalState));
            var infectionCount = 0;
            var currentNode = new Complex((int)initalState.Keys.Max(n => n.Real) / 2, (int)initalState.Keys.Min(n => n.Imaginary) / 2);
            var direction = Complex.ImaginaryOne;
            foreach (var _ in Enumerable.Range(0, 10_000))
            {
                var nodeState = state[currentNode];
                direction *= nodeState ? -Complex.ImaginaryOne : Complex.ImaginaryOne;
                state[currentNode] = !nodeState;
                currentNode += direction;
                if (!nodeState)
                    infectionCount++;
            }
            return infectionCount;
        }

        const int CLEAN = 0;
        const int WEAKENED = 1;
        const int INFECTED = 2;
        const int FLAGGED = 3;
        static Complex[] STATE_DIRECTIONS = new[] {
            Complex.ImaginaryOne,
            1,
            -Complex.ImaginaryOne,
            -1
        };
        static int[] STATE_TRANSITIONS = new[] {
            WEAKENED,
            INFECTED,
            FLAGGED,
            CLEAN
        };
        static int Part2(InfectionStatus initalState)
        {
            var quadState = new DefaultDictionary<Complex, int>(initalState.ToDictionary(pair => pair.Key, pair => pair.Value ? INFECTED : CLEAN));
            var infectionCount = 0;
            var currentNode = new Complex((int)initalState.Keys.Max(n => n.Real) / 2, (int)initalState.Keys.Min(n => n.Imaginary) / 2);
            var direction = Complex.ImaginaryOne;
            foreach (var _ in Enumerable.Range(0, 10_000_000))
            {
                var nodeState = quadState[currentNode];
                var newState = STATE_TRANSITIONS[nodeState];
                direction *= STATE_DIRECTIONS[nodeState];
                quadState[currentNode] = newState;
                currentNode += direction;
                if (newState == INFECTED)
                    infectionCount++;
            }
            return infectionCount;
        }

        static (int, int) Solve(InfectionStatus initalState)
            => (
                Part1(initalState),
                Part2(initalState)
            );

        static InfectionStatus GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var infectionStatus = new InfectionStatus();
            foreach (var (line, y) in File.ReadLines(filePath).Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    infectionStatus[new Complex(x, -y)] = c == '#';
            return infectionStatus;
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
