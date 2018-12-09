import socket
import threading 
import os

def PrintContents(sock):
	sock.send(str(len(os.listdir("/home/vaibhav/ftp"))))
	print "Hello"
	ack=sock.recv(1024)
	print ack
	for x in os.listdir("/home/vaibhav/ftp"):
		sock.send(x)
		ack=sock.recv(1024)
	#sock.send(os.listdir("/home/vaibhav/Desktop"))

def RetrFile(name,sock):
	op=sock.recv(1)
	print op
	sock.send("ack")
	
	if op=='1':  #server to client
		print "Hello"
		ack=sock.recv(1024)
		PrintContents(sock)
		filename = sock.recv(1024)
		if os.path.isfile(filename):
			sock.send("EXIST:"+ str(os.path.getsize(filename)))
			print "Exist"
			userResponse = sock.recv(1024)
			if userResponse[:2] =='OK':
				with open(filename,'rb') as f:
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(1024)
						sock.send(bytesToSend)
		else:
			sock.send("Error in Sending! File doesn't exist")
		sock.close()
	elif op=='2':
		fileToReceive=sock.recv(1024)
		print fileToReceive
		sock.send("ack")
		bytesToReceiveStr=sock.recv(1024)
		sock.send("ack")
		numBytesToReceive = int(bytesToReceiveStr)
		print numBytesToReceive
		f = open('new_' + fileToReceive, 'wb')  #wb is for write binary mode
		data = sock.recv(1024)
		totalRecvd = len(data)
		f.write(data)
		while totalRecvd < numBytesToReceive:
			print "1KB received "
			data = sock.recv(1024)
			totalRecvd += len(data)
			f.write(data)
		print str(len(data)) + " bytes received"
		print "Download Complete"
		

def Main():
	host = '127.0.0.1'
	port = 3333

	s = socket.socket()	#socket.AF_INET and socket.SOCK_STREAM are default arguments
	s.bind((host,port))

	s.listen(5)

	print "Server Started"

	while 1:
		clientSocket, addr = s.accept()
		print "Client Connected with IP addr: " + str(addr)
		t = threading.Thread(target = RetrFile, args = ("retrThread",clientSocket)) 
		t.start()

	s.close()

if __name__ == '__main__':
	Main()
