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


ser = serial.Serial(PORT, 1500000, timeout=0.5, inter_byte_timeout=5)
ser.flushInput()
ser.flushOutput()

while True:
    get_response(ser)
