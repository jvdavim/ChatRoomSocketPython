import socket

HOST = ''              # Server IP address
PORT = 5000            # Server port


#Init socket's variables
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

#Bind socket
tcp_server.bind(server_address)

#Listen clients
tcp_server.listen(5)

#Loop while to connect clients and message delivery
while True:
    con, cliente = tcp_server.accept()
    print 'Concetado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente, msg
    print 'Finalizando conexao do cliente', cliente
    con.close()



    #readable, writable, exceptional = select.select(inputs, outputs, inputs)