from ClientThread import *

#Call client socket thread
client = ClientThread('127.0.0.1',5000)
client.start()