#SUCCESSSSS
import struct
import time
import serial

def main(ser):
	a = 253
	b = 5
	c = 10
	while(True):
		temp = ['h',a] #dengan metode seperti ini, lower order byte dikirimkan terlebih dahulu, berbeda dengan contoh sebelumnya.
		send = struct.pack(*temp)
		print(str(a) + " " + str(send) + " " +str(struct.unpack(temp[0],send)))
		time.sleep(1)
		ser.write(send)
		if(a<258):
			a+=1
		else:
			a=253

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
	main(ser)

'''
def main():
	a = 0
	b = 5
	c = 10
	while(True):
		send = struct.pack('hhh',a,b,c)
		print(str(a) + " " + str(send) + " " +str(struct.unpack('hhh',send)))
		time.sleep(1)
		
		if(a<256):
			a+=1
		else:
			a=0
'''

'''
#OUTPUT

0 b'\x00\x00\x05\x00\n\x00' (0, 5, 10)
1 b'\x01\x00\x05\x00\n\x00' (1, 5, 10)
2 b'\x02\x00\x05\x00\n\x00' (2, 5, 10)
3 b'\x03\x00\x05\x00\n\x00' (3, 5, 10)
4 b'\x04\x00\x05\x00\n\x00' (4, 5, 10)
5 b'\x05\x00\x05\x00\n\x00' (5, 5, 10)
6 b'\x06\x00\x05\x00\n\x00' (6, 5, 10)
7 b'\x07\x00\x05\x00\n\x00' (7, 5, 10)
8 b'\x08\x00\x05\x00\n\x00' (8, 5, 10)
9 b'\t\x00\x05\x00\n\x00' (9, 5, 10)
10 b'\n\x00\x05\x00\n\x00' (10, 5, 10)
11 b'\x0b\x00\x05\x00\n\x00' (11, 5, 10)
12 b'\x0c\x00\x05\x00\n\x00' (12, 5, 10)
13 b'\r\x00\x05\x00\n\x00' (13, 5, 10)
14 b'\x0e\x00\x05\x00\n\x00' (14, 5, 10)
15 b'\x0f\x00\x05\x00\n\x00' (15, 5, 10)
16 b'\x10\x00\x05\x00\n\x00' (16, 5, 10)
17 b'\x11\x00\x05\x00\n\x00' (17, 5, 10)
18 b'\x12\x00\x05\x00\n\x00' (18, 5, 10)
19 b'\x13\x00\x05\x00\n\x00' (19, 5, 10)
20 b'\x14\x00\x05\x00\n\x00' (20, 5, 10)
21 b'\x15\x00\x05\x00\n\x00' (21, 5, 10)
22 b'\x16\x00\x05\x00\n\x00' (22, 5, 10)
23 b'\x17\x00\x05\x00\n\x00' (23, 5, 10)
24 b'\x18\x00\x05\x00\n\x00' (24, 5, 10)
25 b'\x19\x00\x05\x00\n\x00' (25, 5, 10)
26 b'\x1a\x00\x05\x00\n\x00' (26, 5, 10)
27 b'\x1b\x00\x05\x00\n\x00' (27, 5, 10)
28 b'\x1c\x00\x05\x00\n\x00' (28, 5, 10)
29 b'\x1d\x00\x05\x00\n\x00' (29, 5, 10)
30 b'\x1e\x00\x05\x00\n\x00' (30, 5, 10)
31 b'\x1f\x00\x05\x00\n\x00' (31, 5, 10)
32 b' \x00\x05\x00\n\x00' (32, 5, 10)
33 b'!\x00\x05\x00\n\x00' (33, 5, 10)
34 b'"\x00\x05\x00\n\x00' (34, 5, 10)
35 b'#\x00\x05\x00\n\x00' (35, 5, 10)
36 b'$\x00\x05\x00\n\x00' (36, 5, 10)
37 b'%\x00\x05\x00\n\x00' (37, 5, 10)
38 b'&\x00\x05\x00\n\x00' (38, 5, 10)
39 b"'\x00\x05\x00\n\x00" (39, 5, 10)
40 b'(\x00\x05\x00\n\x00' (40, 5, 10)
41 b')\x00\x05\x00\n\x00' (41, 5, 10)
.
.
.
254 b'\xfe\x00\x05\x00\n\x00' (254, 5, 10)
255 b'\xff\x00\x05\x00\n\x00' (255, 5, 10)
256 b'\x00\x01\x05\x00\n\x00' (256, 5, 10)
257 b'\x01\x01\x05\x00\n\x00' (257, 5, 10)
258 b'\x02\x01\x05\x00\n\x00' (258, 5, 10)
254 b'\xfe\x00\x05\x00\n\x00' (254, 5, 10)
255 b'\xff\x00\x05\x00\n\x00' (255, 5, 10)
256 b'\x00\x01\x05\x00\n\x00' (256, 5, 10)
257 b'\x01\x01\x05\x00\n\x00' (257, 5, 10)
258 b'\x02\x01\x05\x00\n\x00' (258, 5, 10)

'''
