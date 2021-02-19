using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class DefaultDictionary<TKey, TValue> : IEnumerable<KeyValuePair<TKey, TValue>>
    {
        public bool Any() => _innerDictionary.Any();
        public IEnumerable<TKey> Keys => _innerDictionary.Keys;

        public DefaultDictionary(Dictionary<TKey, TValue> init = default(Dictionary<TKey, TValue>), Func<TValue> generator = null)
        {
             _innerDictionary = init ?? new Dictionary<TKey, TValue>();
             _generator = generator ?? (() => default(TValue));
        }

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

        public IEnumerator<KeyValuePair<TKey, TValue>> GetEnumerator()
            => _innerDictionary.GetEnumerator();

        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()
            => _innerDictionary.GetEnumerator();

        private IDictionary<TKey, TValue> _innerDictionary;
        private Func<TValue> _generator;
    }

    static class Program
    {
        static int GetManhatanValue(int[] values)
            => values.Sum(value => Math.Abs(value));

        static int Part1(IEnumerable<(int[], int[], int[])> particles)
        {
            var closestParticle = 0;
            var lowestAcceleration = int.MaxValue;
            var lowestPosition = int.MaxValue;
            foreach (var ((position, _, acceleration), index) in particles.Select((particle, index) => (particle, index)))
            {
                var accelerationTotal = GetManhatanValue(acceleration);
                if (accelerationTotal < lowestAcceleration)
                {
                    lowestAcceleration = accelerationTotal;
                    closestParticle = index;
                    lowestPosition = GetManhatanValue(position);
                }
                if (accelerationTotal == lowestAcceleration && GetManhatanValue(position) < lowestPosition)
                {
                    closestParticle = index;
                    lowestPosition = GetManhatanValue(position);
                }
            }
            return closestParticle;
        }

        static (double, double, int) GetQuadraticABC((int[], int[], int[]) particleA, (int[], int[], int[]) particleB, int coordinate)
        {
            var pAp = particleA.Item1[coordinate];
            var pAa = particleA.Item3[coordinate];
            var pAv = particleA.Item2[coordinate] + pAa / 2.0;
            var pBp = particleB.Item1[coordinate];
            var pBa = particleB.Item3[coordinate];
            var pBv = particleB.Item2[coordinate] + pBa / 2.0;
            return ((pAa - pBa) / 2.0, pAv - pBv, pAp - pBp);
        }

        static IEnumerable<int> GetXCollitionTimes((int[], int[], int[]) particleA, (int[], int[], int[]) particleB)
        {
            var (a, b, c) = GetQuadraticABC(particleA, particleB, 0);
            var times = new List<double>();
            if (a == 0)
            {
                if (b != 0)
                    yield return (int)(-c / b);
            }
            else
            {
                var bb = b * b;
                var ac4 = a * c * 4;
                if (bb < ac4)
                    yield break;
                else if (bb == ac4)
                    yield return (int)(-b / (2 * a));
                else 
                {
                    var rt = Math.Sqrt(bb - ac4);
                    var value = (-b + rt) / (2 * a);
                    if (value >= 0 && value % 1 == 0)
                        yield return (int)value;
                    value = (-b - rt) / (2 * a);
                    if (value >= 0 && value % 1 == 0)
                        yield return (int)value;
                }
            }
        }

        static IEnumerable<int> GetCoilitionTimes((int[], int[], int[]) particleA, (int[], int[], int[]) particleB)
        {
            foreach (var time in GetXCollitionTimes(particleA, particleB))
            {
                var collide = true;
                foreach (var k in new [] { 1 , 2 })
                {
                    var (a, b, c) = GetQuadraticABC(particleA, particleB, k);
                    if (a * time * time + b * time + c != 0)
                    {
                        collide = false;
                        break;
                    }
                }
                if (collide)
                    yield return time;
            }
        }
    
        static int Part2(IEnumerable<(int[], int[], int[])> particles)
        {
            var particlesArray = particles.ToArray();
            var collisions = new DefaultDictionary<int, List<(int, int)>>(null, () => new List<(int, int)>());
            for (var thisIndex = 0; thisIndex < particlesArray.Length; thisIndex++)
                for (var otherIndex = thisIndex + 1; otherIndex < particlesArray.Length; otherIndex++)
                    foreach (var time in GetCoilitionTimes(particlesArray[thisIndex], particlesArray[otherIndex]))
                        collisions[time].Add((thisIndex, otherIndex));
            var particleIndexes = Enumerable.Range(0, particlesArray.Length);
            foreach (var time in collisions.Keys.OrderBy(t => t))
            {
                var collidedToRemove = new List<int>();
                foreach (var (indexA, indexB) in collisions[time])
                    if (particleIndexes.Contains(indexA) && particleIndexes.Contains(indexB))
                    {
                        collidedToRemove.Add(indexA);
                        collidedToRemove.Add(indexB);
                    }
                particleIndexes = particleIndexes.Except(collidedToRemove);
            }
            return particleIndexes.Count();
        }

        static Regex lineRegex = new Regex(@"^p=<(?<p>[^>]+)>, v=<(?<v>[^>]+)>, a=<(?<a>[^>]+)>$", RegexOptions.Compiled);
        static IEnumerable<(int[], int[], int[])> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return (
                        match.Groups["p"].Value.Split(",").Select(int.Parse).ToArray(),
                        match.Groups["v"].Value.Split(",").Select(int.Parse).ToArray(),
                        match.Groups["a"].Value.Split(",").Select(int.Parse).ToArray()
                    );
                throw new Exception($"Bad format '{line}'");
            });
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
