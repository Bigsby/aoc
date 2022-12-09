using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = IEnumerable<Tuple<char, int>>;

    static class Program
    {
        static Dictionary<char, Complex> DIRECTIONS = new Dictionary<char, Complex> {
            { 'R', new Complex(1, 0) },
            { 'L', new Complex(-1, 0) },
            { 'U', new Complex(0, 1) },
            { 'D', new Complex(0, -1) },
        };

        static int DoMotions(IEnumerable<Tuple<char, int>> motions, int tailCount)
        {
            var head = Complex.Zero;
            var tails = Enumerable.Range(0, tailCount).Select(_ => Complex.Zero).ToList();
            var visited = new HashSet<Complex>();
            visited.Add(tails.Last());
            foreach (var (direction, length) in motions)
            {
                var directionOffset = DIRECTIONS[direction];
                for (var count = 0; count < length; count++)
                {
                    head += directionOffset;
                    var currentHead = head;
                    for (var index = 0; index < tailCount; index++)
                    {
                        var currentTail = tails[index];
                        var offset = currentHead - currentTail;
                        if (offset == 0)
                            break;
                        if (Math.Abs(offset.Real) > 1)
                            currentTail = new Complex(
                                currentTail.Real + offset.Real / 2,
                                Math.Abs(offset.Imaginary) < 2 ? currentHead.Imaginary : currentTail.Imaginary + offset.Imaginary / 2
                            );
                        else if (Math.Abs(offset.Imaginary) > 1)
                            currentTail = new Complex(
                                Math.Abs(offset.Real) < 2 ? currentHead.Real : currentTail.Real + offset.Real / 2,
                                offset.Imaginary / 2 + currentTail.Imaginary
                            );
                        currentHead = tails[index] = currentTail;
                    }
                    visited.Add(tails.Last());
                }
            }
            return visited.Count;
        }

        static (int, int) Solve(Input motions)
            => (DoMotions(motions, 1), DoMotions(motions, 9));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Split(" ")).Select(split => Tuple.Create(split[0][0], int.Parse(split[1])));

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
