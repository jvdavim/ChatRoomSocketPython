import socket, time, tkMessageBox
from threading import Thread
from Tkinter import *
from tkFileDialog import askopenfilename

class GuiThread(Thread):
	def __init__(self, tcp_client):
		Thread.__init__(self)
		self.tcp_client = tcp_client
		self.running = True

	
	def run(self):
		self.s=Tk()

		self.s.protocol("WM_DELETE_WINDOW", self.on_close)

		self.frame=Frame(self.s, height=500)
		self.s.title("Ez Pz Chat")

		self.buttonframe=Frame(self.s)

		self.imagebutton=Button(text="TRANSFERIR ARQUIVO",bg="#128C7E",fg="white",command=self.sendImage)
		self.imagebutton.pack(in_=self.buttonframe, side=RIGHT)

		self.sendbutton=Button(text="ENVIAR",bg="#075E54",fg="white",command=self.sendText)
		self.sendbutton.pack(in_=self.buttonframe, side=RIGHT)

		self.filebutton=Button(text="CARREGAR TEXTO",bg="#128C7E",fg="white",command=self.sendFile)
		self.filebutton.pack(in_=self.buttonframe, side=RIGHT)

		self.writearea=Text(height=5, width=50)
		self.writearea.pack(in_=self.frame, side=BOTTOM)

		self.textarea=Text(height=25, width=50)
		self.textarea.pack(in_=self.frame)
		self.scrollbar=Scrollbar()
		self.textarea.pack(side=LEFT, fill=Y)
		self.scrollbar.pack(in_=self.frame, side=RIGHT, fill=Y)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(yscrollcommand=self.scrollbar.set)
		self.textarea.config(state=DISABLED)

		self.s.bind("<Return>",self.sendText)
		self.s.bind("<KP_Enter>",self.sendText)
		self.frame.pack()
		self.buttonframe.pack(side=BOTTOM)

		self.s.resizable(width=False,height=False)

		self.writearea.focus_set()

		self.login=Toplevel()
		userframe=Frame(self.login)
		passframe=Frame(self.login)
		loginframe=Frame(self.login)
		label=Label(userframe,text="Nome de usuario:")
		label.pack(side=LEFT)
		self.username=Text(userframe,width=15,height=1)
		self.username.pack(side=LEFT)
		label2=Label(passframe,text="Senha de acesso:")
		label2.pack(side=LEFT)
		self.password=Text(passframe,width=15,height=1)
		self.password.pack(side=LEFT)
		userframe.pack()
		passframe.pack()
		authbutton=Button(loginframe,text="ENTRAR",bg="#25D366",fg="white",command=self.auth)
		authbutton.pack(side=LEFT)
		logup=Button(loginframe,text="CADASTRAR",bg="#25D366",fg="white",command=self.register)
		logup.pack(side=LEFT)
		loginframe.pack()
		# self.login.attributes("-topmost",True)
		self.username.bind("<Return>",self.auth)
		self.username.bind("<KP_Enter>",self.auth)
		self.password.bind("<Return>",self.auth)
		self.password.bind("<KP_Enter>",self.auth)
		self.login.resizable(width=False,height=False)

		self.s.withdraw()
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
		if data[0]=='i':
			data=data[1:]
			self.textarea.config(state=NORMAL)
			self.textarea.insert(END,data.split("\n")[0])
			self.textarea.insert(END,"\n"+data.split("\n")[1])
			self.textarea.insert(END,"\n\t/ARQUIVO RECEBIDO/")
			self.textarea.config(state=DISABLED)
			filename=data.split("\n")[1].split("/")[-1]
			myfile=open(filename,"wb")
			for i in data.split("\n")[2:]:
				myfile.write(i+"\n")
			myfile.close()
		elif data.split(" ")[1]=="OK":
			self.login.destroy()
			self.s.deiconify()
		else:
			self.textarea.config(state=NORMAL)
			self.textarea.insert(END,data.decode("utf-8")+"\n")
			self.textarea.config(state=DISABLED)

	def sendFile(self, event=None):
		path=askopenfilename()
		myfile=open(path,"rb")
		data=myfile.read()
		myfile.close()
		self.tcp_client.send((path+"\n"+data).encode("utf-8"))
		self.textarea.config(state=NORMAL)
		self.textarea.insert(END,"Eu: \n\t"+path+"\n"+data)
		self.textarea.config(state=DISABLED)
		self.textarea.see("end")

	def sendImage(self,event=None):
		path=askopenfilename()
		myfile=open(path,"rb")
		data=myfile.read()
		myfile.close()
		self.tcp_client.send("i"+path+"\n"+data)
		self.textarea.config(state=NORMAL)
		self.textarea.insert(END,"Eu: \n\t"+path+"\n")
		#self.textarea.image_create(END,image=path)
		self.textarea.config(state=DISABLED)
		self.textarea.see("end")

	def auth(self,event=None):
		self.tcp_client.send(("l/"+self.username.get("1.0",END)).encode("utf-8")[:-1]+" "+self.password.get("1.0",END).encode("utf-8"))
		time.sleep(1)

	def register(self,event=None):
		self.tcp_client.send(("c/"+self.username.get("1.0",END)).encode("utf-8")[:-1]+" "+self.password.get("1.0",END).encode("utf-8"))
		time.sleep(1)

	def error_message(self):
		tkMessageBox.showerror("Erro", "Ja existe um usuario com esse login.")

	def successful_message(self):
		tkMessageBox.showinfo("Cadastro", "Cadastro efetuado com sucesso!")

	def on_close(self):
		self.running = False
		self.tcp_client.close()
		self.s.destroy()
		sys.exit(0)