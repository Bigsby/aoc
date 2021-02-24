using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using States = Dictionary<string, ((int, int, string), (int, int, string))>;

    class DefaultDictionary<TKey, TValue>
    {
        public bool Any() => _innerDictionary.Any();
        public IEnumerable<TKey> Keys => _innerDictionary.Keys;
        public IEnumerable<TValue> Values => _innerDictionary.Values;

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
        private Dictionary<TKey, TValue> _innerDictionary = new Dictionary<TKey, TValue>();
    }

    static class Program
    {
        static int Part1((string, int, States) data)
        {
            var (currentState, steps, states) = data;
            var cursor = 0;
            var tape = new DefaultDictionary<int, int>();
            foreach (var _ in Enumerable.Range(0, steps))
            {
                var cursorValue = tape[cursor] == 0;
                var (value, direction, state) = cursorValue ? states[currentState].Item1 : states[currentState].Item2;
                tape[cursor] = value;
                cursor += direction;
                currentState = state;
            }
            return tape.Values.Sum();
        }

        static object Part2(object puzzleInput) => null;

        static Regex setupRegex = new Regex(@"^Begin in state (?<state>\w).*\s+^[^\d]*(?<steps>\d+)", RegexOptions.Compiled | RegexOptions.Multiline);
        static Regex stateRegex = new Regex(@"In state (?<state>\w).*value (?<fValue>\d).* to the (?<fSlot>right|left).*state (?<fState>\w).*value (?<tValue>\d).* to the (?<tSlot>right|left).*state (?<tState>\w)", RegexOptions.Compiled | RegexOptions.Singleline);
        static (string, int, States) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var states = new States();
            var initialState = string.Empty;
            var steps = 0;
            foreach (var split in File.ReadAllText(filePath).Split(Environment.NewLine + Environment.NewLine))
            {
                var setupMatch = setupRegex.Match(split);
                if (setupMatch.Success)
                {
                    initialState = setupMatch.Groups["state"].Value;
                    steps = int.Parse(setupMatch.Groups["steps"].Value);
                    continue;
                }
                var stateMatch = stateRegex.Match(split);
                if (stateMatch.Success)
                    states[stateMatch.Groups["state"].Value] = (
                        (
                            int.Parse(stateMatch.Groups["fValue"].Value),
                            stateMatch.Groups["fSlot"].Value == "right" ? 1 : -1,
                            stateMatch.Groups["fState"].Value
                        ),
                        (
                            int.Parse(stateMatch.Groups["tValue"].Value),
                            stateMatch.Groups["tSlot"].Value == "right" ? 1 : -1,
                            stateMatch.Groups["tState"].Value
                        )
                    );
            }
            return (initialState, steps, states);
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
