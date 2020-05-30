import socket
import sys
import select

clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print "Enter in the order: script, IP address, port number"
    exit()
SERVER_IP=str(sys.argv[1])
SERVER_PORT=int(sys.argv[2])
ADDR=(SERVER_IP,SERVER_PORT)

clientSocket.connect(ADDR)
FORMAT="utf-8"
print("Welcome to the Quiz...To win you have to score atleast 5 points...\nPress any key of the keyboard as a buzzer for the asked question...Good Luck!!\n\n")
while True:
	#List of possible input streams to the clientSocket
	sockets_list=[sys.stdin, clientSocket]
	read_sockets, write_socket, error_socket=select.select(sockets_list,[],[])

	for socket in read_sockets:
		if(socket==clientSocket):
			message=clientSocket.recv(2048).decode(FORMAT)
			print(message)
		else:
			message=sys.stdin.readline()
			clientSocket.send(message.encode(FORMAT))
			sys.stdout.flush()


clientSocket.close()
sys.exit()


