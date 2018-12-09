import socket
import os

def RetrFile(sock):
	#PrintContents(sock)
	filename = raw_input("Enter filename: ")
	
	if os.path.isfile(filename):
		print "EXIST:"+ str(os.path.getsize(filename))
		ch=(raw_input("Upload?(Y/N): "))
		if ch =='Y':
			sock.send(filename)
			ack=sock.recv(1024)
			sock.send(str(os.path.getsize(filename)))
			ack=sock.recv(1024)
			with open(filename,'rb') as f:
				bytesToSend = f.read(1024)
				sock.send(bytesToSend)
				while bytesToSend != "":
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
	else:
		sock.send("Error in Sending! File doesn't exist")
	sock.close()


def Main():
	host = '127.0.0.1'
	port = 3333

	s = socket.socket()
	s.connect((host,port))
	
	
	print "Enter the operation: "
	print "1. Receive"
	print "2. Send"

	choice=int(raw_input("Enter your choice: "))

	if choice==1:
		s.send("1")
		ack=s.recv(1024)
		print ack
		s.send("ack")
		x=s.recv(1024)
		#print x
		s.send("ack")
		print x + " contents:"
		for i in range(int(x)):
			content = s.recv(1024)
			s.send("ack")
			print content
		
		filename = raw_input("Enter the Filename: ")
		s.send(filename)
		data = s.recv(1024)
	
		if data[:6] == 'EXIST:':
			filesize = long(data[6:])
			message = raw_input("File Exist: " + str(filesize) + " Bytes." + " Download? (Y/N): ")
			if(message == 'Y'):
				s.send('OK')
				f = open('new_' + filename, 'wb')  #wb is for write binary mode
				data = s.recv(1024)
				totalRecvd = len(data)
				f.write(data)
				while totalRecvd < filesize:
					print "1KB received "
					data = s.recv(1024)
					totalRecvd += len(data)
					f.write(data)
				print str(len(data)) + " bytes received"
				print "Download Complete"
		else:
			print "The file does not exist!"
		s.close()
	elif choice==2:
		s.send("2")
		ack=s.recv(1024)
		RetrFile(s)

if __name__ == "__main__":
	Main()
			
				 
