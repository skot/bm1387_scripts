import serial
import sys
import time
from crc import *
import math


# nice hex array print
def pretty_hex(data):
	print("[", end='')
	for x in data[:-1]:
		print("%02X " % x, end='')
	print("%02X]" % data[-1])


def send_bytes(obytes, ser):
	obytes.append(crc8(obytes))
	print("Sending: ", end='')
	pretty_hex(obytes)
	ser.write(bytearray(obytes))


def send_bytes16(obytes, ser):
	obytes = obytes + crc16_false(obytes)
	print("Sending: ", end='')
	pretty_hex(obytes)
	ser.write(bytearray(obytes))

def frequency_setting(frequency):
	buffer = [0x58, 0x09, 0x00, 0x0C, 0x00, 0x50, 0x02, 0x41]   # 250MHz -- osc of 25MHz
	if frequency < 50:
		frequency = 50
	elif frequency > 900:
		frequency = 900
	frequency = int(math.ceil(100 * (frequency) / 625.0) * 6.25);

	if (frequency < 400):
		buffer[7] = 0x41
		buffer[5] = int((frequency * 8) / 25)
	elif (frequency < 600):
		buffer[7] = 0x21
		buffer[5] = int((frequency * 4) / 25)
	else:
		buffer[7] = 0x11
		buffer[5] = int((frequency * 2) / 25)
	return buffer


def get_response(ser):
	counter = 0
	while ser.inWaiting() < 0:
		time.sleep(0.001)
		counter += 1
		if (counter > 20):
			return
	input_bytes = ser.read(100) #read more than enough packets. we are counting on hitting inter_byte_timeout
	
	if (len(list(input_bytes)) > 0):
		pretty_hex(list(input_bytes))



if (len(sys.argv) == 2):
	PORT = sys.argv[1]

else:
	print("Hax0rs the bitcoin")
	print("Usage: %s [SERIAL PORT]" % sys.argv[0])
	exit()


ser = serial.Serial(PORT, 115200, timeout=0.5, inter_byte_timeout=1)
ser.flushInput()
ser.flushOutput()

send_bytes([0x58, 0x09, 0x00, 0x1C, 0x00, 0x20, 0x19, 0x00], ser)
time.sleep(0.01)

send_bytes([0x54, 0x05, 0x00, 0x00], ser)
get_response(ser)
time.sleep(0.01)

send_bytes(frequency_setting(100), ser)
time.sleep(0.01)

send_bytes([0x41, 0x05, 0x00, 0x00], ser)
time.sleep(0.01)

send_bytes([0x41, 0x05, 0x80, 0x00], ser)
time.sleep(0.01)

send_bytes([0x58, 0x09, 0x00, 0x1C, 0x40, 0x20, 0x99, 0x80], ser)
time.sleep(0.01)

for x in range(0x74):
	send_bytes16([0x21, 0x36, x, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], ser)
	time.sleep(0.005)

send_bytes16([0x21, 0x36, 0x74, 0x01, 0x00, 0x00, 0x00, 0x00, 0xF9, 0x1E, 0x0E, 0x17, 0x80, 0x20, 0xCC, 0x60, 0x61, 0x81, 0x55, 0x05, 0x00, 0x36, 0x06, 0x53, 0x32, 0x62, 0xA2, 0x41, 0x21, 0xA0, 0x3C, 0xB2, 0x43, 0xE3, 0xC0, 0x53, 0x49, 0xFC, 0x20, 0x7A, 0x9D, 0x5D, 0xE0, 0x84, 0xE6, 0x62, 0x14, 0x75, 0x99, 0xCB, 0x96, 0x9C], ser)
get_response(ser)

send_bytes16([0x21, 0x36, 0x75, 0x01, 0x00, 0x00, 0x00, 0x00, 0xF9, 0x1E, 0x0E, 0x17, 0x80, 0x20, 0xCC, 0x60, 0x2B, 0x2A, 0xD6, 0x7D, 0x12, 0x9C, 0x99, 0x8C, 0x0C, 0x69, 0x06, 0x2B, 0xBE, 0x67, 0xC3, 0xE4, 0x35, 0xEA, 0xDC, 0xF5, 0xFF, 0xAA, 0xDF, 0x9A, 0xF0, 0xEB, 0x7F, 0xCE, 0xE6, 0x8A, 0x50, 0x96, 0xEF, 0xD5, 0x96, 0x44], ser)
get_response(ser)

