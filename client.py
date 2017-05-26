import socket
import sys
import select
import userlib


#class Client(Thread)

HOST = '127.0.0.1'     # Server IP address
PORT = 5000            # Server port

#Init socket's variables
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

#Connect to server
tcp_client.connect(dest)
print 'Para sair use CTRL+X\n'

msg = raw_input()
while msg <> '\x18':
    tcp_client.send (msg)
    msg = raw_input()
tcp_client.close