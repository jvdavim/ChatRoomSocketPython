import socket
from threading import Thread
from Tkinter import *
from tkFileDialog import askopenfilename

class GuiThread(Thread):
	def __init__(self, tcp_client):
		Thread.__init__(self)
		self.tcp_client = tcp_client
	
	def run(self):
		self.s=Tk()

		self.frame=Frame(self.s, height=500)
		self.s.title("Ez Pz Chat")

		self.imagebutton=Button(text="TRANSFERIR ARQUIVO",bg="#128C7E",fg="white",command=self.sendFile)
		self.imagebutton.pack(side=BOTTOM)

		self.sendbutton=Button(text="ENVIAR",bg="#128C7E",fg="white",command=self.sendText)
		self.sendbutton.pack(side=BOTTOM)

		self.writearea=Text(height=5, width=50)
		self.writearea.pack(side=BOTTOM)

		self.textarea=Text(height=25, width=50)
		self.textarea.pack()
		self.scrollbar=Scrollbar()
		self.textarea.pack(side=LEFT, fill=Y)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(yscrollcommand=self.scrollbar.set)
		self.textarea.config(state=DISABLED)

		self.s.bind("<Return>",self.sendText)
		self.s.bind("<KP_Enter>",self.sendText)
		self.frame.pack()

		self.writearea.focus_set()

		self.s.mainloop()

	def sendText(self, event=None):
	    msg = self.writearea.get("1.0",END)
	    self.tcp_client.send(msg.encode("utf-8"))
	    self.textarea.config(state=NORMAL)
	    self.textarea.insert(END,"Eu: \n\t"+msg)
	    self.textarea.config(state=DISABLED)
	    self.textarea.see("end")
	    self.writearea.delete("1.0",END)

	def show(self, data):
		self.textarea.config(state=NORMAL)
		self.textarea.insert(END,data.decode("utf-8"))
		self.textarea.config(state=DISABLED)

	def isRunning(self):
		if self.s.state() != 'normal':
			return False
		return True

	def sendFile(self, event=None):
	    path=askopenfilename()
	    self.tcp_client.send(path.encode("utf-8"))
	    self.textarea.config(state=NORMAL)
	    self.textarea.insert(END,"Eu: \n\t"+path)
	    self.textarea.config(state=DISABLED)
	    self.textarea.see("end")
