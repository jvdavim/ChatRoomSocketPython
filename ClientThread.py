import socket, os
from threading import Thread
from GuiThread import *

class ClientThread(Thread):
    def __init__(self,HOST,PORT):
        Thread.__init__(self)
        self.host = HOST
        self.port = PORT

    def run(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = (self.host, self.port)
        self.tcp_client.connect(self.dest)
        self.gui = GuiThread(self.tcp_client)
        self.gui.start()
        while True:
            self.data = self.tcp_client.recv(1024)
            self.gui.show(self.data)
	    self.gui.textarea.see("end")
	    #os.system("play --no-show-progress --null --channels 1 synth 1 sine 1000")


