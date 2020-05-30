import socket
import select
import sys
import random
import time
from _thread import *
import threading
FORMAT="utf-8"

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if(len(sys.argv)!=3):
	print("Enter in the order: script, IP address, port number")
	exit()

SERVER_IP=str(sys.argv[1])
SERVER_PORT=int(sys.argv[2])
ADDR=(SERVER_IP,SERVER_PORT)

serverSocket.bind(ADDR)
serverSocket.listen(20)

Ques= ["Which planet has the 'Great Red Spot'? \n a.Saturn  b.Uranus  c.Neptune  d.Jupiter\n",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit  b.Celsius  c.Kelvin  d.Rankine\n",
     " Which sea creature has three hearts? \n a.Dolphin  b.Octopus  c.Walrus  d.Seal\n",
     " Which is the largest river in India? \n a.Ganga  b.Yamuna  c.Tapti  d.Narmada\n",
     " How many bones does an adult human have? \n a.206  b.208  c.201  d.196\n",
     " How many wonders are there in the world? \n a.7  b.8  c.9  d.4\n",
     " Which is the lightest metal? \n a.Li  b.Na  c.K  d.He\n",
     " How many union territories are there in India? \n a.9  b.8  c.6  d.7\n",
     " Which is the largest Indian state? \n a.Rajasthan  b.Maharashtra  c.Bihar  d.Madhya Pradesh\n",
     " Who is the inventor of Electricity? \n a.Marconi  b.T.A.Edison  c.Benjamin Franklin  d.Alexander Graham Bell\n",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams b.Kalpana Chawla c.None of them d.Both of them\n ",
     " What is the smallest continent? \n a.Asia  b.Antarctic  c.Africa  d.Australia\n",
     " Which continent is known as the 'Dark' continent? \n a.Asia  b.Antartica  c.Europe  d.Africa\n",
     " How many players in a team of volleyball? \n a.6  b.7  c.9  d.8\n",
     " Hg stands for? \n a.Mercury  b.Hulgerium  c.Argenine  d.Halfnium\n",
     " How many cricket world cups does India have? \n a.0  b.1  c.2  d.3\n",
     " Which planet is closest to the sun? \n a.Mercury b.Pluto c.Earth d.Venus\n",
     " How many spokes are on the Chakra in the Indian Flag? \n a.24  b.26  c.28  d.30\n",
     " Mount Everest is located in which of these country? \n a.India  b.Nepal  c.Tibet  d.China\n",
     " The Gateway of India is in which of these city?\n a.Chennai  b.Mumbai  c.Kolkata  d.New Delhi\n"]


Ans = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'a', 'a', 'c', 'a', 'a', 'b', 'b']
list_of_clients=[]				#List of active connections
scores=[]						#Stores the scores of each player
buzzer=[0,0]					#buzzer[0] tells if the buzzer is pressed or not and buzzer[1] stores the index of the current question 
client=["",-1]					#Stores the details of the client who has pressed the buzzer
send_msg=""


def clientthread(connectionSocket,addr):
	while True:
		if(len(list_of_clients)==3):
			message=connectionSocket.recv(64).decode(FORMAT)
			if message:
				if buzzer[0]==0:
					client[0]=connectionSocket
					buzzer[0]=1
					i=0
					while i<len(list_of_clients):
						if(list_of_clients[i]==connectionSocket):
							break
						i+=1
					client[1]=i

				elif buzzer[0]==1 and client[0]==connectionSocket:
					if(message[0]==Ans[buzzer[1]][0]):
						#Correct answer is given
						send_except(connectionSocket,"--> Player " + str(client[1]+1) + " scored a +1 for the above question\n\n")
						send_msg="--> You (Player " + str(client[1]+1)+ ") have scored a +1 for the above question\n\n"
						connectionSocket.send(send_msg.encode(FORMAT))

						scores[i]=scores[i]+1
						#Wins the quiz by scoring atleast 5 points
						if(scores[i]>=5):
							send_to_all("QUIZ HAS ENDED!!\n\n")
							send_except(connectionSocket,"--> Player " + str(client[1]+1) + " has WON the Quiz!!!\n\n")
							send_msg="--> You (Player " + str(client[1]+1)+ ") have WON the Quiz!!!\n\n"
							connectionSocket.send(send_msg.encode(FORMAT))
							end_quiz()
							sys.exit()

					else: 
						#Incorrect answer is given
						send_except(connectionSocket,"--> Player " + str(client[1]+1) + " got a -0.5 for the above question\n\n")
						send_msg="--> You (Player " + str(client[1]+1) + ") got a -0.5 for the above question\n\n"
						connectionSocket.send(send_msg.encode(FORMAT))
						scores[i]= scores[i]-(1/2)

					buzzer[0]=0
					if(len(Ques)!=0):
						Ques.pop(buzzer[1])
						Ans.pop(buzzer[1])

					if(len(Ques)==0):
						send_to_all("QUIZ HAS ENDED!!\n\n")
						end_quiz()
						sys.exit()
					else:
						begin_quiz()

				else:
					send_msg="--> Sorry! Player "+str(client[1]+1)+" pressed the buzzer first...\n\n"
					connectionSocket.send(send_msg.encode(FORMAT))


			else:
				remove_connection(connectionSocket)

def end_quiz():
	if(max(scores)<5):
		send_to_all("IT IS A TIE...(As none of the players could score atleast 5 points to win)\n\n")
	send_to_all("The final scores are as follows:\n")
	for x in range(len(list_of_clients)):
		send_to_all("-->Player " + str(x+1) + " scored " + str(scores[x]) + " points\n")
	send_to_all("\n\nTHANKS FOR PLAYING...\n")
	serverSocket.close()
	

#This function is called for removing a connection
def remove_connection(connectionSocket):
	if connectionSocket in list_of_clients:
		list_of_clients.remove(connectionSocket)


#This function sends the message to all active connections
def send_to_all(message):
	for clients in list_of_clients:
		try:
			clients.send(message.encode(FORMAT))
		except:
			clients.close()
			remove(clients)


#This function send the nessage to all the other active clients except the connection passed as the parameter
def send_except(conn,message):
	for clients in list_of_clients:
		if(conn!=clients):
			try:
				clients.send(message.encode(FORMAT))
			except:
				clients.close()
				remove(clients)

def begin_quiz():
	buzzer[1]=random.randint(0,10000)%len(Ques)
	if(len(Ques)!=0):
		for connection in list_of_clients:
			connection.send(Ques[buzzer[1]].encode(FORMAT))


while True:
	connectionSocket, addr=serverSocket.accept()
	list_of_clients.append(connectionSocket)
	print(addr[0] + ' : Player ' +str(list_of_clients.index(connectionSocket)+1)  + ' connected\n')
	scores.append(0)
	start_new_thread(clientthread,(connectionSocket, addr))
	if(len(list_of_clients)==3):
		begin_quiz()

connectionSocket.close()
serverSocket.close()