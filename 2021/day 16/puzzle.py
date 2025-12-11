
with open("input") as f:
    input = f.read()

hexmap = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

def hex_to_bin(hex):
    return "".join([hexmap[x] for x in hex])

def read_packet(packet):
    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)
    packet = packet[6:]
    # literal
    if type_id == 4:
        bits = []
        while packet.startswith("1"):
            bits.append(packet[1:5])
            packet = packet[5:]
        bits.append(packet[1:5])
        packet = packet[5:]
        return int("".join(bits), 2), packet
    else:
        length_id = int(packet[0])
        packet = packet[1:]
        values = []
        if length_id == 0:
            total_length = int(packet[:15], 2)
            packet = packet[15:]

            subpacket_buffer, packet = packet[:total_length], packet[total_length:]
            while subpacket_buffer:
                value, subpacket_buffer = read_packet(subpacket_buffer)
                values.append(value)
        else:
            total_packets = int(packet[:11], 2)
            packet = packet[11:]
            for i in range(total_packets):
                value, packet = read_packet(packet)
                values.append(value)
        
        if type_id == 0:
            return sum(values), packet
        elif type_id == 1:
            val = 1
            for v in values:
                val *= v
            return val, packet
        elif type_id == 2:
            return min(values), packet
        elif type_id == 3:
            return max(values), packet
        elif type_id == 5:
            return int(values[0] > values[1]), packet
        elif type_id == 6:
            return int(values[0] < values[1]), packet
        elif type_id == 7:
            return int(values[0] == values[1]), packet

def read_hex_packet(packet):
    return read_packet(hex_to_bin(packet))

print(read_hex_packet(input))
