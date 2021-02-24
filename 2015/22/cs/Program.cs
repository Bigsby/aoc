using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Spell = Tuple<int, int, int, int, int, int>;
    static class Program
    {
        static Spell[] SPELLS = new [] {
            Tuple.Create(53,  4, 0, 0,   0, 0), // Magic Missile
            Tuple.Create(73,  2, 2, 0,   0, 0), // Drain
            Tuple.Create(113, 0, 0, 7,   0, 6), // Shield
            Tuple.Create(173, 3, 0, 0,   0, 6), // Poison
            Tuple.Create(229, 0, 0, 0, 101, 5)  // Recharge            
        };

        static int GetLeastWinningMana(int initialBossHit, int bossDamage, bool loseHitOnPlayerTurn)
        {
            var leastManaSpent = int.MaxValue;
            var queue = new Stack<(int, int, int, IEnumerable<Spell>, bool, int)>();
            queue.Push((initialBossHit, 50, 500, new Spell[0], true, 0));
            while (queue.Any())
            {
                var (bossHit, playerHit, playerMana, activeSpells, playerTurn, manaSpent) = queue.Pop();
                if (loseHitOnPlayerTurn && playerTurn)
                { 
                    playerHit--;
                    if (playerHit <= 0)
                        continue;
                }
                var playerArmor = 0;
                var newActiveSpells = new List<Spell>();
                foreach (var activeSpell in activeSpells)
                {
                    var (cost, damage, hitPoints, armor, mana, duration) = activeSpell;
                    if (duration >= 0)
                    {
                        bossHit -= damage;
                        playerHit += hitPoints;
                        playerArmor += armor;
                        playerMana += mana;
                    }
                    if (duration > 1)
                        newActiveSpells.Add(Tuple.Create(cost, damage, hitPoints, armor, mana, duration - 1));
                }
                if (bossHit <= 0)
                {
                    leastManaSpent = Math.Min(leastManaSpent, manaSpent);
                    continue;
                }
                if (manaSpent > leastManaSpent)
                    continue;
                if (playerTurn)
                {
                    var activeCosts = newActiveSpells.Select(spell => spell.Item1); // cost is unique per spell
                    foreach (var spell in SPELLS)
                    {
                        var spellCost = spell.Item1;
                        if (!activeCosts.Contains(spellCost) && spellCost <= playerMana)
                            queue.Push((bossHit, playerHit, playerMana - spellCost, newActiveSpells.Concat(new [] { spell }), false, manaSpent + spellCost));
                    }
                }
                else
                {
                    playerHit -= Math.Max(1, bossDamage - playerArmor);
                    if (playerHit > 0)
                        queue.Push((bossHit, playerHit, playerMana, newActiveSpells, true, manaSpent));
                }
            }
            return leastManaSpent;
        }


        static int Part1((int bossHit, int bossDamage) data)
            => GetLeastWinningMana(data.bossHit, data.bossDamage, false);

        static int Part2((int bossHit, int bossDamage) data)
            => GetLeastWinningMana(data.bossHit, data.bossDamage, true);

        static (int, int) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var matches = Regex.Matches(File.ReadAllText(filePath), @"(\d+)").ToArray();
            return (int.Parse(matches[0].Value), int.Parse(matches[1].Value));
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
