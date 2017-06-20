import select, socket, sys, Queue, time, signal, ssl

#Exit handler
def signal_handler(signal, frame):
	print "\nSuccessful exit. Server is now down."
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def broadcast_data (sock, message):
	#Do not send the message to master socket and the client who has send us the message
	for socket in inputs:
		if socket != tcp_server and socket != sock:
			try :
				socket.send(message)
			except :
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				inputs.remove(socket)

def send_data_to(sock, message):
	#Do not send the message to master socket and the client who has send us the message
	for socket in inputs:
		if socket == sock:
			try :
				socket.send(message)
			except :
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				inputs.remove(socket)


HOST = ''			  # Server IP address
PORT = 5000			# Server port

#Init socket's variables
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sslcontext = ssl._create_unverified_context()
sslcontext.load_cert_chain(certfile="server.crt", keyfile="server.key")
tcp_server.setblocking(0)
server_address = (HOST, PORT)

#Bind socket
tcp_server.bind(server_address)

#Listen clients
tcp_server.listen(5)

#Declare sockets lists and queues
inputs = [tcp_server]
outputs = []
message_queues = {}
users={}

print "Successful creation. Server is now up."

#Loop while to connect clients and message delivery
while inputs:
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	for s in readable:
		if s is tcp_server:
			connection, client_address = s.accept()
			sslcon=sslcontext.wrap_socket(connection, server_side=True)
			sslcon.setblocking(0)
			inputs.append(sslcon)
			message_queues[sslcon] = Queue.Queue()
		else:
			data = s.recv(1024)
			print str(client_address)+": "+data
			if data:
				message_queues[s].put(data)
				if s not in outputs:
					outputs.append(s)
			else:
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()
				del message_queues[s]

	for s in writable:
		try:
			next_msg = message_queues[s].get_nowait()
		except Queue.Empty:
			outputs.remove(s)
		else:
			if next_msg[:2]=='i/':
				broadcast_data(s,"i"+users[str(client_address)]+" diz:\n\t"+next_msg[1:])
			elif next_msg[:2]=="l/":
				users[str(client_address)]=next_msg[2:-1].decode("utf-8")
				f=open("users.txt","r")
				for i in f.readlines():
					if next_msg[2:]==i:
						broadcast_data(s,i.split(" ")[0]+" entrou na sala.")
						send_data_to(s,"OK OK")
				f.close()
			elif next_msg[:2]=="c/":
				f=open("users.txt","r+")
				conflict=False
				for i in f.readlines():
					if i.split(" ")[0]==next_msg[2:].split(" ")[0]:
						conflict=True
				if conflict:
					print "Ja Existe"
				else:
					f.write(next_msg[2:])
				f.close()
			else:
				broadcast_data(s,users[str(client_address)]+" diz:\n\t"+next_msg)

	for s in exceptional:
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()
		del message_queues[s]

tcp_server.close()
