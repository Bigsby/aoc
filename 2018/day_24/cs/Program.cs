using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Group
    {
        public string Id { get; init; }
        public int Units { get; set; }
        public int HitPoints { get; init; }
        public IEnumerable<string> Immunities { get; init; }
        public IEnumerable<string> Weaknesses { get; init; }
        public int Initiative { get; init; }
        public string Type { get; init; }
        public int Damage { get; init; }
        public int Army { get; init; }
        public int EffectivePower => Units * Damage;
        public Group Target { get; set; }

        public Group(string id, int units, int hit, IEnumerable<string> immunities, 
            IEnumerable<string> weaknesses, int initiative, string type, int damage, int army)
        {
            Id = id;
            Units = units;
            HitPoints = hit;
            Immunities = immunities;
            Weaknesses = weaknesses;
            Initiative = initiative;
            Type = type;
            Damage = damage;
            Army = army;
        }

        public int DamageTo(Group target)
            => target.Immunities.Contains(Type) ? 0
                : EffectivePower * (target.Weaknesses.Contains(Type) ? 2 : 1);
        
        public Group Clone(int boost)
            => new Group(Id, Units, HitPoints, Immunities, Weaknesses, Initiative, Type, Damage + boost, Army);
    }

    static class Program
    {
        static (int winner, int unitsLeft) Combat(IEnumerable<Group> initialGroups, int boost)
        {
            var groups = initialGroups.Select(group => group.Clone(group.Army == 0 ? boost : 0)).ToArray();
            while (true)
            {
                groups = groups.OrderByDescending(group => group.EffectivePower).ThenByDescending(group => group.Initiative).ToArray();
                var selectedTargets = new List<string>();
                var ts = new Dictionary<string, string>();

                foreach (var group in groups)
                {
                    var targets = groups.Where(target => target.Army != group.Army && !selectedTargets.Contains(target.Id) && group.DamageTo(target) > 0);
                    if (targets.Any())
                    {
                        group.Target = targets.OrderByDescending(target => group.DamageTo(target))
                                            .ThenByDescending(target => target.EffectivePower)
                                            .ThenByDescending(target => target.Initiative).First();
                        selectedTargets.Add(group.Target.Id);
                    }
                }
                groups = groups.OrderByDescending(group => group.Initiative).ToArray();
                var unitsKilled = false;
                foreach (var group in groups)
                    if (group.Target is not null)
                    {
                        var killed = Math.Min(group.Target.Units, group.DamageTo(group.Target) / group.Target.HitPoints);
                        unitsKilled |= killed > 0;
                        group.Target.Units -= killed;
                    }
                groups = groups.Where(group => group.Units > 0).ToArray();
                foreach (var group in groups)
                    group.Target = null;
                var immuneSystemUnits = groups.Where(group => group.Army == 0).Sum(group => group.Units);
                var infectionUnits = groups.Where(group => group.Army == 1).Sum(group => group.Units);
                if (!unitsKilled || immuneSystemUnits == 0)
                    return (1, infectionUnits);
                if (infectionUnits == 0)
                    return (0, immuneSystemUnits);
            }
        }

        static int Part1(IEnumerable<Group> groups) => Combat(groups, 0).unitsLeft;

        static int Part2(IEnumerable<Group> groups)
        {
            var boost = 0;
            while (true)
            {
                var (winner, left) = Combat(groups, ++boost);
                if (winner == 0)
                    return left;
            }
        }

        static Regex numbersRegex = new Regex(@"^(?<units>\d+) units.*with (?<hit>\d+) hit.*does (?<damage>\d+) (?<type>\w+).*initiative (?<initiative>\d+)$", RegexOptions.Compiled);
        static Regex immunityWeaknessRegex = new Regex(@"\(.*\)", RegexOptions.Compiled);
        static Group ParseGroup(string text, int army, int number)
        {
            var nummbersMatch = numbersRegex.Match(text);
            if (nummbersMatch.Success)
            {
                var immunities = new List<string>();
                var weaknesses = new List<string>();
                var immunityWeaknessMatch = immunityWeaknessRegex.Match(text);
                if (immunityWeaknessMatch.Success)
                    foreach (var group in immunityWeaknessMatch.Value[1..^1].Split(";").Select(group => group.Trim()))
                        if (group.StartsWith("weak"))
                            weaknesses.AddRange(group[8..].Split(',').Select(t => t.Trim()));
                        else if (group.StartsWith("immune"))
                            immunities.AddRange(group[10..].Split(',').Select(t => t.Trim()));
                return new Group(
                    $"{army}{number}",
                    int.Parse(nummbersMatch.Groups["units"].Value),
                    int.Parse(nummbersMatch.Groups["hit"].Value),
                    immunities, weaknesses,
                    int.Parse(nummbersMatch.Groups["initiative"].Value),
                    nummbersMatch.Groups["type"].Value,
                    int.Parse(nummbersMatch.Groups["damage"].Value),
                    army
                );
            }
            throw new Exception($"Bad format '{text}'");
        }

        static IEnumerable<Group> ParseArmy(string text, int army)
            => text.Split("\n").Skip(1).Select((groupText, index) => ParseGroup(groupText, army, index + 1));

        static IEnumerable<Group> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var armyTexts = File.ReadAllText(filePath).Split("\n\n");
            var immuneSystem = ParseArmy(armyTexts[0], 0);
            var infection = ParseArmy(armyTexts[1], 1);
            return immuneSystem.Concat(infection);

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
