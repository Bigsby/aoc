#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <limits.h>

typedef char* Input;
typedef struct
{
    int part1;
    unsigned long part2;
} Results;

typedef enum 
{
    Sum,
    Product,
    Minimum,
    Maximum,
    Literal,
    Greater,
    Less,
    Equals
} PacketTypes;

typedef struct Packet
{
    int version;
    unsigned long value;
    PacketTypes type;
    int packetCount;
    struct Packet *subPackets;

} Packet;

char *getPacket(char *message, Packet *packet);

char *getNBits(char *message, int count, int *value)
{
    *value = 0;
    while (count--)
        *value = (*value << 1) + (*message++ == '1'); 
    return message;
}

char *getSubPackets(char *message, int *count, Packet **subPackets)
{
    int lengthId;
    message = getNBits(message, 1, &lengthId);
    Packet packet;
    Packet *packets;
    if (lengthId)
    {
        message = getNBits(message, 11, count);
        packets = malloc((*count) * sizeof(Packet));
        for (int index = 0; index < *count; index++)
        {
            message = getPacket(message, &packet);
            packets[index] = packet;
        }
    } else
    {
        message = getNBits(message, 15, count);
        int capacity = 2;
        int size = 0;
        int startingLength = strlen(message);
        packets = malloc(capacity * sizeof(Packet));
        while (startingLength - strlen(message) < *count - 1)
        {
            if (size == capacity)
                packets = realloc(packets, (capacity += 2) * sizeof(Packet));
            message = getPacket(message, &packet); 
            packets[size++] = packet;
        }
        *count = size;
    }
    *subPackets = packets;
    return message;
}

char *getPacket(char *message, Packet *packet)
{
    int version, type;
    unsigned long value;
    message = getNBits(message, 3, &version);
    message = getNBits(message, 3, &type);
    packet->version = version;
    packet->type = (PacketTypes)type;
    packet->value = 0;
    packet->packetCount = 0;
    packet->subPackets = NULL;
    if (type == 4)
    {
        value = 0;
        int notFinal, partial;
        while (1)
        {
            message = getNBits(message, 1, &notFinal);
            message = getNBits(message, 4, &partial);
            value = (value << 4) +  partial;
            if (!notFinal)
                break;
        }
        packet->value = value;
    } else
        message = getSubPackets(message, &(packet->packetCount), &(packet->subPackets));
    return message;
}

int getPacketVersionSum(Packet packet)
{
    int version = packet.version;
    while (packet.packetCount--)
        version += getPacketVersionSum(*packet.subPackets++);
    return version;
}

unsigned long getPacketValue(Packet packet)
{
    unsigned long value, subValue;
    switch (packet.type)
    {
        case Literal:
            return packet.value;
        case Sum:
            value = 0;
            while (packet.packetCount--)
                value += getPacketValue(*packet.subPackets++);
            return value;
        case Product:
            value = 1;
            while (packet.packetCount--)
                value *= getPacketValue(*packet.subPackets++);
            return value;
        case Minimum:
            value = INT_MAX;
            while (packet.packetCount--)
            {
                subValue = getPacketValue(*packet.subPackets++);
                value = value < subValue ? value : subValue;
            }
            return value;
        case Maximum:
            value = 0;
            while (packet.packetCount--)
            {
                subValue = getPacketValue(*packet.subPackets++);
                value = value > subValue ? value : subValue;
            }
            return value;
        case Greater:
            return getPacketValue(packet.subPackets[0]) > getPacketValue(packet.subPackets[1]);
        case Less:
            return getPacketValue(packet.subPackets[0]) < getPacketValue(packet.subPackets[1]);
        case Equals:
            return getPacketValue(packet.subPackets[0]) == getPacketValue(packet.subPackets[1]);
    }
    perror("Uknown type");
    exit(1);
}


Results solve(Input message)
{
    Packet *packet = malloc(sizeof(packet));
    message = getPacket(message, packet);
    return (Results){getPacketVersionSum(*packet), getPacketValue(*packet)};
}

Input getInput(char *filePath)
{
    FILE *file;
    if ((file = fopen(filePath, "r")) == NULL)
    {
        perror("Error reading input file!\n");
        exit(1);
    }
    fseek(file, 0, SEEK_END);
    long length = ftell(file) - 1;
    Input input = malloc(length * 4 * sizeof(char));
    rewind(file);
    char *content = malloc(length);
    fread(content, 1, length, file);
    unsigned char value;
    for (int index = 0; index < length; index += 2)
    {
        sscanf(content + index, "%2hhx", &value);
        for (int bit = 0; bit < 8; bit++)
            input[index * 4 + bit] = (1 << (7 - bit)) & value ? '1' : '0';
    }
    fclose(file);
    return input;
}

void freeInput(Input input)
{
    free(input);
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        perror("Please, add input file path as parameter");
        exit(1);
    }
    struct timeval starts, ends;
    gettimeofday(&starts, NULL);
    Input input = getInput(argv[1]);
    Results results = solve(input);
    gettimeofday(&ends, NULL);
    freeInput(input);
    printf("P1: %d\n", results.part1);
    printf("P2: %lu\n\n", results.part2);
    printf("Time: %.7f\n", (double)((ends.tv_sec - starts.tv_sec) * 1000000 + ends.tv_usec - starts.tv_usec) / 1000000);
    return 0;
}
