'''
File ini mendemonstrasikan perbedaan tentang byte order pada struct python
'''

import struct
import time
import serial

def main(ser):
	a = 258
	while(True):
		temp = ['>h',a] #untuk lebih dari satu data, penulisan > cukup sekali, contoh '>hhh'
		send = struct.pack(*temp)
		print(str(a) + " " + str(send) + " " +str(struct.unpack(temp[0],send)))
		time.sleep(1)
		ser.write(send)
	

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
	main(ser)

'''
jika temp = ['<h',a]
258 b'\x02\x01' (258,) #low order terlebih dahulu |little-endian

jika temp = ['>h',a]
258 b'\x01\x02' (258,) #high order terlebih dahulu |big-endian

'''
