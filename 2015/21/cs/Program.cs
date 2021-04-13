using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Player = Tuple<int, int, int>;

    static class Program
    {
        static IEnumerable<(int, int, int)> WEAPONS = new[] {
            (8, 4, 0),
            (10, 5, 0),
            (25, 6, 0),
            (40, 7, 0),
            (74, 8, 0)
        };
        static IEnumerable<(int, int, int)> ARMORS = new[] {
            (0, 0, 0),
            (13, 0, 1),
            (31, 0, 2),
            (53, 0, 3),
            (75, 0, 4),
            (102, 0,5)
        };
        static IEnumerable<(int, int, int)> RINGS = new[] {
            (0, 0, 0),
            (0, 0, 0),
            (25, 1, 0),
            (50, 2, 0),
            (100, 3, 0),
            (20, 0, 1),
            (40, 0, 2),
            (80, 0, 3)
        };

        static bool PlayGame(Player player, Player boss)
        {
            var (playerHit, playerDamage, playerArmor) = player;
            var (bossHit, bossDamage, bossArmor) = boss;
            playerDamage = Math.Max(1, playerDamage - bossArmor);
            bossDamage = Math.Max(1, bossDamage - playerArmor);
            while (true)
            {
                bossHit -= playerDamage;
                if (bossHit <= 0)
                    return true;
                playerHit -= bossDamage;
                if (playerHit <= 0)
                    return false;
            }
        }

        static IEnumerable<T[]> Combinations<T>(IEnumerable<T> source, int length)
        {
            T[] result = new T[length];
            Stack<int> stack = new Stack<int>();
            var data = source.ToArray();
            stack.Push(0);
            while (stack.Count > 0)
            {
                int resultIndex = stack.Count - 1;
                int dataIndex = stack.Pop();
                while (dataIndex < data.Length)
                {
                    result[resultIndex++] = data[dataIndex];
                    stack.Push(++dataIndex);
                    if (resultIndex == length)
                    {
                        yield return result;
                        break;
                    }
                }
            }
        }

        static IEnumerable<(int, int, int)> GetInventoryCombinations()
        {
            foreach (var weapon in WEAPONS)
                foreach (var armor in ARMORS)
                    foreach (var rings in Combinations(RINGS, 2))
                    {
                        var inventory = new[] { weapon, armor, rings[0], rings[1] };
                        yield return inventory
                            .Aggregate((soFar, current) => 
                                (soFar.Item1 + current.Item1, soFar.Item2 + current.Item2, soFar.Item3 + current.Item3));
                    }
        }

        static (int, int) Solve(Player boss)
        {
            var minCost = int.MaxValue;
            var maxCost = 0;
            foreach (var (cost, damage, defense) in GetInventoryCombinations())
                if (PlayGame(Tuple.Create(100, damage, defense), boss))
                    minCost = Math.Min(minCost, cost);
                else
                    maxCost = Math.Max(maxCost, cost);
            return (minCost, maxCost);
        }

        static Player GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var match = Regex.Match(File.ReadAllText(filePath), @"^Hit Points: (?<hit>\d+)\W+Damage: (?<damage>\d+)\W+^Armor: (?<armor>\d+)", RegexOptions.Multiline);
            return Tuple.Create(
                int.Parse(match.Groups["hit"].Value),
                int.Parse(match.Groups["damage"].Value),
                int.Parse(match.Groups["armor"].Value)
            );
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
