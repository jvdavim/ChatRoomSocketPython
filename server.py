import select, socket, sys, Queue, time, signal, ssl


def signal_handler(signal, frame):
	#Trata sinal para saida
	print "\nSuccessful exit. Server is now down."
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def broadcast_data (sock, message):
	#Envia mensagem para todos os clientes menos para si mesmo
	for socket in inputs:
		if socket != tcp_server and socket != sock:
			try :
				socket.send(message)
			except :
				#Falha na conexao com o cliente
				socket.close()
				inputs.remove(socket)

def send_data_to(sock, message):
	#Envia mensagem para um cliente especifico
	for socket in inputs:
		if socket == sock:
			try :
				socket.send(message)
			except :
				#Falha na conexao com o cliente
				socket.close()
				inputs.remove(socket)


HOST = ''			  # Server IP address
PORT = 5000			# Server port

#Inicializa variaveis para o socket
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sslcontext = ssl._create_unverified_context()
sslcontext.load_cert_chain(certfile="server.crt", keyfile="server.key")
tcp_server.setblocking(0)
server_address = (HOST, PORT)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Da bind na porta
tcp_server.bind(server_address)

#Fica em estado listen aguardando clientes
tcp_server.listen(5)

#Declaracao de listas e filas de sockets, mensagens e usuarios
inputs = [tcp_server]
outputs = []
message_queues = {}
users={}

print "Successful creation. Server is now up."

#Loop while para realizar a conexao com os clientes e entregar as mensagens
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
			data = s.recv(4096)
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
				broadcast_data(s,"i"+users[s]+" diz:\n\t"+next_msg[1:])
			elif next_msg[:2]=="l/":
				users[s]=next_msg[2:].split(" ")[0]
				with open("users.txt","r") as f:
					failure=True
					for i in f:
						if next_msg[2:]==i.rstrip("\n"):
							broadcast_data(s,i.split(" ")[0]+" entrou na sala.")
							send_data_to(s,"OK OK")
							failure=False
					if failure:
						send_data_to(s,"f/")
					f.close()
			elif next_msg[:2]=="c/":
				with open("users.txt","r+") as f:
					conflict=False
					for i in f:
						if i.rstrip("\n").split(" ")[0]==next_msg[2:].split(" ")[0]:
							conflict=True
					if conflict:
						send_data_to(s,"e/")
					else:
						f.write(next_msg[2:]+"\n")
						send_data_to(s,"s/")
					f.close()
			elif next_msg[:2]=="m/":
				next_msg=next_msg[2:]
				answer = (users[s]+" diz:\n\t")+(next_msg.decode("utf-8"))
				broadcast_data(s,answer.encode("utf-8"))

	for s in exceptional:
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()
		del message_queues[s]

tcp_server.close()
