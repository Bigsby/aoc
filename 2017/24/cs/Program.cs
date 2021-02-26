using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    static class Program
    {
        static (int, int) Max((int, int) a,  (int, int) b)
        {
            if (a.Item1 > b.Item1)
                return a;
            if (a.Item1 == b.Item1)
                return a.Item2 > b.Item2 ? a : b;
            return b;
        }

        static bool Equal((int, int) a,  (int, int) b)
            => a.Item1 == b.Item1 && a.Item2 == b.Item2;

        static bool Connects((int port1, int port2) component, int port)
            => component.port1 == port || component.port2 == port;

        static (int, int) Solve(IEnumerable<(int port1, int port2)> components)
        {
            var starts = components.Where(component => Connects(component, 0));
            var stack = new Stack<(int, int, IEnumerable<(int port1, int port2)>)>();
            foreach (var start in starts)
                stack.Push((start.port1 == 0 ? start.port2 : start.port1, 0, new [] { start }));
            var longestStrongest1 = (0, 0);
            var longestStrongest2 = (0, 0);
            while (stack.Any())
            {
                var (lastPort, strength, used) = stack.Pop();
                var continued = false;
                foreach (var component in components.Where(
                    component => Connects(component, lastPort) && !used.Any(u => Equal(u, component))))
                {
                    continued = true;
                    var nextPort = component.port1 == component.port2 ? lastPort : (component.port1 == lastPort ? component.port2 : component.port1);
                    var newUsed = used.ToList();
                    newUsed.Add(component);
                    stack.Push((nextPort, strength + lastPort * 2, newUsed));
                }
                if (!continued)
                {
                    longestStrongest1 = Max(longestStrongest1, (0, strength + lastPort));
                    longestStrongest2 = Max(longestStrongest2, (used.Count(), strength + lastPort));
                }
            }
            return (longestStrongest1.Item2, longestStrongest2.Item2);
        }

        static IEnumerable<(int, int)> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var split = line.Split('/');
                return (
                    int.Parse(split[0]),
                    int.Parse(split[1])
                );
            });

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
