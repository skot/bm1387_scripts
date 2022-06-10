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
	print("Sending:  ", end='')
	pretty_hex(obytes)
	ser.write(bytearray(obytes))


def send_bytes16(obytes, ser):
	obytes = obytes + crc16_false(obytes)
	print("Sending:  ", end='')
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

def baudrate(bauddiv):
	baudrate = [0x58, 0x09, 0x00, 0x1C, 0x00, 0x20, 0x07, 0x00, 0x19]
	baudrate[6] = bauddiv
	return baudrate

def gateclk(bauddiv):
	gateclk = [0x58, 0x09, 0x00, 0x1C, 0x40, 0x20, 0x99, 0x80, 0x01]
	gateclk[6] = 0x80 | bauddiv
	return gateclk

def get_response(ser):
	counter = 0
	while ser.inWaiting() < 0:
		time.sleep(0.005)
		counter += 1
		if (counter > 20):
			return
	input_bytes = ser.read(100) #read more than enough packets. we are counting on hitting inter_byte_timeout

	if (len(list(input_bytes)) > 0):
		print("Response: ", end='')
		pretty_hex(list(input_bytes))



if (len(sys.argv) == 2):
	PORT = sys.argv[1]

else:
	print("Hax0rs the bitcoin")
	print("Usage: %s [SERIAL PORT]" % sys.argv[0])
	exit()



ser = serial.Serial(PORT, 115200, timeout=0.5, inter_byte_timeout=5)
ser.flushInput()
ser.flushOutput()

bauddiv = 0x19 # 115200
#bauddiv = 0x0D # 214286
#bauddiv = 0x07 # 375000

# get chip count
send_bytes([0x54, 0x05, 0x00, 0x00], ser)
get_response(ser)
time.sleep(0.01)

# # send frequency
# send_bytes(frequency_setting(50), ser)
# get_response(ser)
# time.sleep(0.01)

# send chip inactive
send_bytes([0x55, 0x05, 0x00, 0x00], ser)
time.sleep(0.01)

# send chip inactive
send_bytes([0x55, 0x05, 0x00, 0x00], ser)
time.sleep(0.01)

# send chip inactive
send_bytes([0x55, 0x05, 0x00, 0x00], ser)
time.sleep(0.01)

# set address
send_bytes([0x41, 0x05, 0x00, 0x00], ser)
get_response(ser)
time.sleep(0.01)

# set address
send_bytes([0x41, 0x05, 0x80, 0x00], ser)
get_response(ser)
time.sleep(0.01)

# set baudrate
send_bytes(baudrate(bauddiv), ser)
time.sleep(0.01)

# gateclk ??
send_bytes(gateclk(bauddiv), ser)
time.sleep(0.01)


for x in range(0x74):
	send_bytes16([0x21, 0x36, x, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], ser)
	# get_response(ser)
	time.sleep(0.005)

send_bytes16([0x21, 0x36, 0x74, 0x01, 0x00, 0x00, 0x00, 0x00, 0xF9, 0x1E, 0x0E, 0x17, 0x80, 0x20, 0xCC, 0x60, 0x61, 0x81, 0x55, 0x05, 0x00, 0x36, 0x06, 0x53, 0x32, 0x62, 0xA2, 0x41, 0x21, 0xA0, 0x3C, 0xB2, 0x43, 0xE3, 0xC0, 0x53, 0x49, 0xFC, 0x20, 0x7A, 0x9D, 0x5D, 0xE0, 0x84, 0xE6, 0x62, 0x14, 0x75, 0x99, 0xCB, 0x96, 0x9C], ser)
get_response(ser)
time.sleep(0.01)

send_bytes16([0x21, 0x36, 0x75, 0x01, 0x00, 0x00, 0x00, 0x00, 0xF9, 0x1E, 0x0E, 0x17, 0x80, 0x20, 0xCC, 0x60, 0x3A, 0xEC, 0xC0, 0x17, 0x48, 0xC5, 0x54, 0x38, 0x05, 0x06, 0x1A, 0xA3, 0x45, 0xD7, 0x4C, 0xA1, 0x0D, 0xB6, 0x44, 0x5F, 0x0C, 0x85, 0x62, 0xF2, 0x97, 0xB4, 0xAE, 0x27, 0x03, 0x33, 0xAB, 0xEE, 0x11, 0xA8, 0x93, 0x5C], ser)
get_response(ser)
time.sleep(0.01)
