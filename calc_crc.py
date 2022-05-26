from crc import *

yo = "21:36:00:01:00:00:00:00:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"
INPUT = [int(x, 16) for x in yo.split(":")]


# nice hex array print
def pretty_hex(data):
	print("[", end='')
	for x in data[:-1]:
		print("%02X " % x, end='')
	print("%02X]" % data[-1])


# calculates the BM1387 CRC for ptr array
def crc_calc(ptr):
	c = [1, 1, 1, 1, 1]
	ptr_idx = 0

	for i in range(8 * len(ptr)):
		c1 = c[1]
		c[1] = c[0]
		c[0] = c[4] ^ (1 if (ptr[ptr_idx] & (0x80 >> (i % 8))) else 0);
		c[4] = c[3]
		c[3] = c[2]
		c[2] = c1 ^ c[0]

		if (((i + 1) % 8) == 0):
			ptr_idx+=1

	return (c[4] * 0x10) | (c[3] * 0x08) | (c[2] * 0x04) | (c[1] * 0x02) | (c[0] * 0x01)


# appends the CRC on the end of the data array
# INPUT[6] = INPUT[6] | 0x19
INPUT = INPUT + crc16_false(INPUT)
pretty_hex(INPUT)


