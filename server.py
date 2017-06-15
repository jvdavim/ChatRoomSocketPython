import select, socket, sys, Queue, time, signal

# Exit handler #
def signal_handler(signal, frame):
    print "\nSuccesful exit"
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
# Exit handler #

def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in inputs:
        if socket != tcp_server and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                inputs.remove(socket)


HOST = ''              # Server IP address
PORT = 5000            # Server port

#Init socket's variables
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

#Loop while to connect clients and message delivery
while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is tcp_server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
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
        	broadcast_data(s,str(client_address)+" diz:\n\t"+next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]

tcp_server.close()