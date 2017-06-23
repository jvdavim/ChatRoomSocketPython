import socket, os, ssl
from threading import Thread
from GuiThread import *

class ClientThread(Thread):
	def __init__(self,HOST,PORT):
		Thread.__init__(self)
		self.host = HOST
		self.port = PORT
		self.sslcontext=ssl._create_unverified_context()

	def run(self):
		self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sslcon=self.sslcontext.wrap_socket(self.tcp_client, server_hostname="127.0.0.1")
		self.dest = (self.host, self.port)
		self.sslcon.connect(self.dest)
		self.gui = GuiThread(self.sslcon)
		self.gui.start()
		while self.gui.running:
			self.data = self.sslcon.recv(2048)
			if self.data == "e/":
				self.gui.error_message()
			elif self.data == "s/":
				self.gui.successful_message()
			elif self.data == "f/":
				self.gui.failedlogin_message()
			else:
				self.gui.show(self.data)
			self.gui.textarea.see("end")
		print "Successful exit."
		sys.exit(0)
			#os.system("play --no-show-progress --null --channels 1 synth 1 sine 1000")  #BARUHLHO
