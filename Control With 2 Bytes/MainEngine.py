import sys
import time
import datetime as dtime
import matplotlib.pyplot as plt
import serial
import struct

import config as cf
from RobotEngine import *
from VisualEngine import *
from ImProcEngine import *

N = cf.N
Period = cf.Period
lt = 0
ltold = 0

def init_robot():	
	#tempq = [90, 90, 150, 90, 90, 90]
	tempq = [0, 0, 0, 0, 0, 0]
	cf.q = [radians(i) for i in tempq]
	
def transmit():
	tempTransmit = [0 for x in range(7)]

	def limit(p):
		if(p>180):
			p=180
		elif(p<0):
			p=0
		return p
		
	#Joint 1
	tempTransmit[0] = -int(degrees(cf.q[0]))+90
	
	#Joint 2
	tempTransmit[1] = -int(degrees(cf.q[1]))+90
	
	#Joint 3
	tempTransmit[2] = int(degrees(cf.q[2]))+90
	
	#Joint 4
	tempTransmit[3] = -int(degrees(cf.q[3]))+90
	
	#Joint 5
	tempTransmit[4] = -int(degrees(cf.q[4]))+90
	
	#Joint 6
	tempTransmit[5] = -int(degrees(cf.q[5]))+90
	
	#Gripper
	tempTransmit[6] = cf.grip
	
	saturatedTransmit = [limit(x) for x in tempTransmit]
	
	temp = ['>hhhhhhh',*saturatedTransmit]
	send = struct.pack(*temp)
	ser.write(b'\xF5') #Header
	ser.write(send) #Data
	
def cetak():
	print("Q_Awal		=  {}".format([round(degrees(p),3) for p in cf.q_awal]))
	print("Q_Sekarang	=  {}".format([round(degrees(p),3) for p in cf.q]))
	print("Q_Final 	=  {}".format([round(degrees(p),3) for p in cf.q_final]))
	print("X_Awal 		=  {}".format([round(p,3) for p in cf.xyz_init]))
	print("X_Sekarang 	=  {}".format([round(p,3) for p in cf.xyz]))
	print("X_Final 	=  {}".format([round(p,3) for p in cf.xyz_final]))
	
def Sim_main():
	logger = []
	loggery = []
	loggerz = []
	
	logcmda = []
	logcmdb = []
	logcmdc = []
	
	if(cf.CamBased == 1):
		cf.k = 0.0;
		tracking()
		if(cf.Fobj):
			cf.q_awal = cf.q[:]
			a = (cf.posr[1]-cf.Yobj) * (1.0 /cf.DimensiFrame[1]) # (Titik pusat objek - pusat frame) * m/px
			b = (cf.posr[0]-cf.Xobj) * (1.34/cf.DimensiFrame[0])
			#print("Cam {} | {} | {} | {}".format(cf.Xobj,cf.Yobj,cf.dXobj,cf.dYobj))
			print("Cam {} | {} | {} | {}".format(cf.Xobj,cf.Yobj,round(a,3),round(b,3)))
			
			'''cf.posa = find()
			a = (270-cf.posa[0]) * (1.0 /cf.DimensiFrame[1]) # (Titik pusat objek - pusat frame) * m/px
			b = (171-cf.posa[1]) * (1.34/cf.DimensiFrame[0])
			print("POSA {} | {} | {} | {}".format(cf.Xobj,cf.Yobj,round(a,3),round(b,3)))'''
		else:
			print("Objek tidak ditemukan")
		if cv2.waitKey(1) & 0xFF == ord("c"):
			cv2.destroyAllWindows()
			cf.CamBased = -1
			tracking()
			
	#Refresh	
	if(cf.refresh == 1):
		tampilkan()
		cetak()
		cf.refresh = 0
		
	#Return to Base
	if(cf.retbase == 1):
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("RETURN TO BASE")
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0;
		trajectory_init()
		temp = [0,70,-20,0,0,0]
		cf.q_final = [radians(x) for x in temp]
		a = dtime.datetime.now()
		
		while(cf.k <= N):
			for p in range(0,6):
				control_joint(p)
			cf.k += 1
			forward_kinematic()
			tampilkan()
			if(cf.k%10 == 0):
				transmit()
		cf.grip = 20
		transmit() #++++++++++++++++++++++++++++++++++++++
			
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		cf.retbase = 0;
		
	#Joint Space
	if(cf.JS != -1) :
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("Joint Space : Joint({}), qAwal({}), qfinal({})".format(cf.JS, [round(degrees(p),3) for p in cf.q_awal], [round(degrees(p),3) for p in cf.q_final]))
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0
		trajectory_init()
		a = dtime.datetime.now()
		while(cf.k <= N):
			n1 = dtime.datetime.now()
			# Logging
			logger.append(degrees(cf.q[cf.JS]))
			control_joint(cf.JS)
			logcmda.append(degrees(cf.q_cmd[cf.JS]))
			forward_kinematic()
			cf.k += 1
			tampilkan()
			transmit()
			n2 = dtime.datetime.now()
			n3 = n2-n1
			temp = 0.0199-n3.total_seconds()*1
			if(temp<0):
				temp = 0
			#time.sleep(temp)
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		plt.plot(logger,"orange",logcmda,"purple")
		plt.legend(["Q Actual", "Q Cmd"])
		plt.suptitle('Joint Control', fontsize=12)
		plt.xlabel('Step', fontsize=12)
		plt.ylabel('Sudut', fontsize=12)
		plt.show()
		cf.JS = -1;
		
	#Task Space	
	if(cf.TS != -1) :
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		print("Task Space")
		print("++++++++++++++++++++++++++++++++++++++++++++++++")
		cf.k = 0.0
		a = dtime.datetime.now()
		trajectory_init()
		
		while(cf.k <= N):
			n1 = dtime.datetime.now()
			#print("+++ {}".format(cf.k))
			
			#Logging
			logger.append(cf.xyz[0])
			loggery.append(cf.xyz[1])
			loggerz.append(cf.xyz[2])
			
			#Proses
			trajectory_planning()
			
			logcmda.append(cf.xyz_cmd[0])
			logcmdb.append(cf.xyz_cmd[1])
			logcmdc.append(cf.xyz_cmd[2])
			
			double_differential()
			control_task()
			inverse_jacobian()
			double_integrator()
			forward_kinematic()
			
			transmit()
			n2 = dtime.datetime.now()
			n3 = n2-n1
			temp = 0.0199-n3.total_seconds()*1
			if(temp<0):
				temp = 0
			#time.sleep(temp)
			
			cf.k += 1
			tampilkan()
			
		b = dtime.datetime.now()
		c = b-a
		print("Elapsed Time : {} ms".format(c.total_seconds()*1000))
		plt.plot(logger,'g-',loggery,'r-', loggerz, 'b-', logcmda,"purple",logcmdb,"purple",logcmdc,"purple")
		plt.legend(["X Actual", "Y Actual", "Z Actual", "XYZ Ref"])
		plt.suptitle('Task Control', fontsize=12)
		plt.xlabel('Step', fontsize=12)
		plt.ylabel('Posisi', fontsize=12)
		plt.show()
		cf.TS = -1
	
	#Bergerak menuju objek
	if(cf.xyobjek != -1):
		
		#Moving X,Y
		trajectory_init()
		cf.xyz_final = cf.xyz[:]
		cf.k = 0.0;
		
		#Interpolasi
		cf.posa = find()

		u = dtime.datetime.now()
		f = dtime.datetime.now()
		g = f-u
		while(g.total_seconds()*1000 < 500):
			f = dtime.datetime.now()
			(grabbed, frame) = cf.camera.read()
			g = f-u				

		cf.posb = find()
		
		dy = cf.posb[0] - cf.posa[0]
		dx = cf.posb[1] - cf.posa[1]
		cf.posc[0] = cf.posb[0] + dy*8
		cf.posc[1] = cf.posb[1] + dx*8
		#print(cf.posa)
		#print(cf.posb)
		#print(cf.posc)
		
		
		if(cf.Fobj):
			#print("Cam {} | {}".format(cf.Xobj,cf.Yobj))
			
			a = dtime.datetime.now()
			trajectory_init()
			
			#Positioning calculation
			#Sumbu X Positif Robot ke atas; Kamera ke Kanan
			e1 = (cf.posr[1]-cf.posc[0]) * (1.0 /cf.DimensiFrame[1]) # (Titik pusat objek - pusat frame) * m/px
			e2 = (cf.posr[0]-cf.posc[1]) * (1.34/cf.DimensiFrame[0])
			cf.xyz_final[0] = e1
			cf.xyz_final[1] = e2+0.1
			#print(e1,e2)
			#print(cf.xyz)
			
			#print("Sesudah Retbase Sebelum XY")
			#cetak()
			while(cf.k <= N):
				#logger.append(cf.xyz[0])
				#loggery.append(cf.xyz[1])
				#loggerz.append(cf.xyz[2])
				n1 = dtime.datetime.now()
				#Proses
				trajectory_planning()
				double_differential()
				control_task()
				inverse_jacobian()
				double_integrator()
				forward_kinematic()				
				
				cf.k += 1
				forward_kinematic()
				tampilkan()
				transmit() #++++++++++++++++++++++++++++++++++++++
				n2 = dtime.datetime.now()
				n3 = n2-n1
				temp = 0.0199-n3.total_seconds()*1
				if(temp<0):
					temp = 0
				time.sleep(temp)
			b = dtime.datetime.now()
			c = b-a
			print("XY Elapsed Time : {} ms".format(c.total_seconds()*1000))
			#plt.plot(logger,'g-',loggery,'r-', loggerz, 'b-')
			#plt.legend(["X", "Y", "Z"])
			#plt.show()
			
			#Dropping
			trajectory_init()
			cf.xyz_final = cf.xyz[:]
			cf.k = 0
			
			a = dtime.datetime.now()
			
			#Positioning calculation
			cf.xyz_final[2] -= 0.1
			#cf.xyz_final[2] -= 0.2
			#print("Sesudah XY Sebelum Z")
			#cetak()
			
			while(cf.k <= N):
				#logger.append(cf.xyz[0])
				#loggery.append(cf.xyz[1])
				#loggerz.append(cf.xyz[2])
				n1 = dtime.datetime.now()
				#Proses
				trajectory_planning()
				double_differential()
				control_task()
				inverse_jacobian()
				double_integrator()
				forward_kinematic()				
				
				cf.k += 1
				forward_kinematic()
				tampilkan()
				transmit() #++++++++++++++++++++++++++++++++++++++
				n2 = dtime.datetime.now()
				n3 = n2-n1
				temp = 0.0199-n3.total_seconds()*1
				if(temp<0):
					temp = 0
				time.sleep(temp)
			b = dtime.datetime.now()
			c = b-a
			print("Z Elapsed Time : {} ms".format(c.total_seconds()*1000))
			print("Selesai")
			cetak()
			#plt.plot(logger,'g-',loggery,'r-', loggerz, 'b-')
			#plt.legend(["X", "Y", "Z"])
			#plt.show()
			
		else:
			print("Objek tidak ditemukan")

		cf.xyobjek = -cf.xyobjek
		
		cf.grip = 80
		transmit() #++++++++++++++++++++++++++++++++++++++
	
	#Simulasi Gerak 
	if(cf.jalan == 1):
		cf.k = 0
		while(cf.k <= N):
			cf.mxyz[0] = cf.mxyz[0] - (0.5/N)
			cf.bxyz[0] = cf.mxyz[0]
			cf.k += 1
			tampilkan()
		cf.jalan = 0
		

def keyPressed(key, x, y):
	global CamBased
	forward_kinematic()
	cf.q_final = cf.q[:]
	cf.xyz_final = cf.xyz[:]
	
	ch = key.decode("utf-8")
	
	# JIka ditekan tombol escape
	if ch == chr(27):
		cf.camera.release() #jangan lupa direlease
		cv2.destroyAllWindows()
		sys.exit()
		
	# Return to base
	elif ch == 'z':
		cf.retbase = 1
	# Refresh
	elif ch == 'x':
		cf.refresh = 1
	# Toggling 
	elif ch == 'c':
		cf.CamBased = -cf.CamBased
		
	#Joint space
	elif ch == 'a':
		cf.q_final[0] += radians(10)
		cf.JS = 0
	elif ch == 'A':
		cf.q_final[0] += -radians(10)
		cf.JS = 0
	elif ch == 's':
		cf.q_final[1] += radians(10)
		cf.JS = 1
	elif ch == 'S':
		cf.q_final[1] += -radians(10)
		cf.JS = 1
	elif ch == 'd':
		cf.q_final[2] += radians(10)
		cf.JS = 2
	elif ch == 'D':
		cf.q_final[2] += -radians(10)
		cf.JS = 2
	elif ch == 'f':
		cf.q_final[3] += radians(10)
		cf.JS = 3
	elif ch == 'F':
		cf.q_final[3] += -radians(10)
		cf.JS = 3
	elif ch == 'g':
		cf.q_final[4] += radians(10)
		cf.JS = 4
	elif ch == 'G':
		cf.q_final[4] += -radians(10)
		cf.JS = 4
	elif ch == 'h':
		cf.q_final[5] += radians(10)
		cf.JS = 5
	elif ch == 'H':
		cf.q_final[5] += -radians(10)
		cf.JS = 5
		
	#Task Space
	elif ch == 'q':
		cf.xyz_final[0]	+= 0.1
		cf.TS = 1
	elif ch == 'w':
		cf.xyz_final[1]	+= 0.1
		cf.TS = 1
	elif ch == 'e':
		cf.xyz_final[2]	+= 0.1
		cf.TS = 1
	elif ch == 'Q':
		cf.xyz_final[0]	-= 0.1
		cf.TS = 1
	elif ch == 'W':
		cf.xyz_final[1]	-= 0.1
		cf.TS = 1
	elif ch == 'E':
		cf.xyz_final[2]	-= 0.1
		cf.TS = 1
	
	#ETC
	elif ch == 'v':
		plt.plot(logger,'g-',loggery,'r-', loggerz, 'b-')
		plt.legend(["X", "Y", "Z"])
		plt.show()
		plt.plot(loggera,'g-',loggerb,'r-', loggerc, 'b-')
		plt.legend(["Psi", "Theta", "Phi"])
		plt.show()
	elif ch == 'b':
		cf.grip = 30
		transmit()
	elif ch == 'n':
		cf.xyobjek = -cf.xyobjek
	
def init():
	glClearColor(1,1,1,1)
	glClear(GL_COLOR_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(40.0, 1, 0.2, 8)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	pencahayaan()
	
	glShadeModel(GL_SMOOTH)
	
	glutDisplayFunc(tampilkan)
	glutKeyboardFunc(keyPressed)
	
def main():
	global window
	
	glutInit(sys.argv)
	
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	
	glutInitWindowSize(400,400)
	glutInitWindowPosition(40,100)
	
	window = glutCreateWindow("6 DOF Robot Controller")
	
	init_robot()
	init()
	
	glutIdleFunc(Sim_main)
	
	glutMainLoop()
	
if __name__ == "__main__":
	ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port
	cf.camera = cv2.VideoCapture(0) #untuk ganti kamera selanjutnya ganti angka 1
	print("%%% Controller 6 DOF %%%")
	print("%%%Warming Up Camera!%%%")
	
	#Progress Bar
	toolbar_width = 20 #2 Sec
	sys.stdout.write("[%s]" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
	for i in range(toolbar_width):
		time.sleep(0.1) # do real work here
		# update the bar
		sys.stdout.write("#")
		sys.stdout.flush()
	sys.stdout.write("\n")
	#End of progress bar
	
	(grab, frame) = cf.camera.read()
	cf.DimensiFrame[0] = frame.shape[1]	
	cf.DimensiFrame[1] = frame.shape[0]
	if not grab:
		print("Gagal mengambil gambar dari kamera")
	
	print("Mulai!")
	main()
