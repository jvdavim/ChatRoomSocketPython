from GUI import *

HOST = '127.0.0.1'     # Server IP address
PORT = 5000            # Server port

#Init socket's variables
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

tcp_client.connect(dest)	#Connect to server

#Call GUI thread
gui = GuiThread(tcp_client)
gui.start()

while True:
    data = tcp_client.recv(1024)
    gui.show(data)

tcp_client.close()