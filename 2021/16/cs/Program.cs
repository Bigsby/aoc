using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text;

namespace AoC
{
    enum PacketType
    {
        Sum,
        Product,
        Minimum,
        Maximum,
        Literal,
        Greater,
        Less,
        Equals
    }

    struct Packet
    {
        public readonly int Version { get; init; }
        public readonly PacketType Type { get; init; }

        public long Value { get; set; }

        public readonly List<Packet> SubPackets { get; }

        public Packet(int version, PacketType type)
        {
            Version = version;
            Type = type;
            Value = 0;
            SubPackets = new List<Packet>();
        }

        public int GetVersionSum()
            => Version + SubPackets.Sum(subPacket => subPacket.GetVersionSum());
        
        public long GetValue()
        {
            switch (Type)
            {
                case PacketType.Literal:
                    return Value;
                case PacketType.Sum:
                    return SubPackets.Sum(subPacket => subPacket.GetValue());
                case PacketType.Product:
                    return SubPackets.Aggregate(1L, (soFar, current) => soFar * current.GetValue());
                case PacketType.Minimum:
                    return SubPackets.Min(subPacket => subPacket.GetValue());
                case PacketType.Maximum:
                    return SubPackets.Max(subPacket => subPacket.GetValue());
                case PacketType.Greater:
                    return SubPackets[0].GetValue() > SubPackets[1].GetValue() ? 1L : 0;
                case PacketType.Less:
                    return SubPackets[0].GetValue() < SubPackets[1].GetValue() ? 1L : 0;
                case PacketType.Equals:
                    return SubPackets[0].GetValue() == SubPackets[1].GetValue() ? 1L : 0;
                default:
                    throw new ArgumentException($"Unknow type {Type}");
            }
        }
    }

    static class Program
    {
        static (string, int) GetNBits(this string message, int count)
        {
            int value = 0;
            for (int index = 0; index < count; index++)
                value = (value << 1) | (message[index] == '1' ? 1 : 0);
            return (message.Substring(count), value);
        }

        static (string, IEnumerable<Packet>) ParseSubPackets(string message)
        {
            var subPackets = new List<Packet>();
            (message, var lengthId) = message.GetNBits(1);
            if (lengthId == 1)
            {
                (message, var packetCount) = message.GetNBits(11);
                while (packetCount-- > 0)
                {
                    (message, var subPacket) = ParsePacket(message);
                    subPackets.Add(subPacket);
                }
            }
            else
            {
                (message, var subPacketsBits) = message.GetNBits(15);
                var startLength = message.Length;
                while (startLength - message.Length < subPacketsBits - 1)
                {
                    (message, var subPacket) = ParsePacket(message);
                    subPackets.Add(subPacket);
                }
            }
            return (message, subPackets);
        }

        static (string, Packet) ParsePacket(string message)
        {
            (message, var version) = message.GetNBits(3);
            (message, var type) = message.GetNBits(3);
            var packet = new Packet(version, (PacketType)type);
            if ((PacketType)type == PacketType.Literal)
            {
                long value = 0;
                while (true)
                {
                    (message, var toContinue) = message.GetNBits(1);
                    (message, var parial) = message.GetNBits(4);
                    value = (value << 4) + parial;
                    if (toContinue == 0)
                        break;
                }
                packet.Value = value;
            }
            else
            {
                (message, var subPackets) = ParseSubPackets(message);
                packet.SubPackets.AddRange(subPackets);
            }
            return (message, packet);
        }

        static (int, long) Solve(string message)
        {
            (message, var packet) = ParsePacket(message);
            return (packet.GetVersionSum(), packet.GetValue());
        }

        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var content = File.ReadAllText(filePath).Trim();
            var message = new StringBuilder();
            for (int index = 0; index < content.Length; index += 2)
                message.Append(Convert.ToString(Convert.ToByte(content.Substring(index, 2), 16), 2).PadLeft(8, '0'));
            return message.ToString();
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
