using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        const string CENTER_OF_MASS = "COM";

        static int Part1(Dictionary<string, string> planetOrbits)
        {
            var planets = new HashSet<string>();
            foreach (var pair in planetOrbits)
            {
                planets.Add(pair.Key);
                planets.Add(pair.Value);
            }
            var orbitCounts = new Dictionary<string, int> { { CENTER_OF_MASS, 0 } };
            while (orbitCounts.Count != planets.Count)
                foreach (var planet in planets)
                {
                    if (orbitCounts.ContainsKey(planet))
                        continue;
                    if (planetOrbits.ContainsKey(planet))
                    {
                        var orbitedPlanet = planetOrbits[planet];
                        if (orbitCounts.ContainsKey(orbitedPlanet))
                            orbitCounts[planet] = orbitCounts[orbitedPlanet] + 1;
                    }
                    else
                        orbitCounts[planet] = 1;
                }
            return orbitCounts.Values.Sum();
        }

        static List<string> GetRevesedPathToCenterOfMass(string planet, Dictionary<string, string> planetOrbits)
        {
            var route = new List<string>();
            while (planet != CENTER_OF_MASS)
            {
                planet = planetOrbits[planet];
                route.Add(planet);
            }
            route.Reverse();
            return route;
        }

        const string YOU = "YOU";
        const string SAN = "SAN";
        static int Part2(Dictionary<string, string> planetOrbits)
        {
            var youPath = GetRevesedPathToCenterOfMass(YOU, planetOrbits);
            var sanPath = GetRevesedPathToCenterOfMass(SAN, planetOrbits);
            while (youPath.First() == sanPath.First())
            {
                youPath.RemoveAt(0);
                sanPath.RemoveAt(0);
            }
            return youPath.Count + sanPath.Count;
        }

        static (int, int) Solve(Dictionary<string, string> planetOrbits)
            => (
                Part1(planetOrbits),
                Part2(planetOrbits)
            );

        static Regex lineRegex = new Regex(@"^(?<orbited>[A-Z\d]{3})\)(?<orbiter>[A-Z\d]{3})$", RegexOptions.Compiled);
        static Dictionary<string, string> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return (match.Groups["orbited"].Value, match.Groups["orbiter"].Value);
                throw new Exception($"Bad format '{line}'");
            }).ToDictionary(pair => pair.Item2, pair => pair.Item1);

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