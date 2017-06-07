from Tkinter import *

def sendText(event=None):
    textarea.config(state=NORMAL)
    textarea.insert(END,"Fulano diz: \n\t"+writearea.get("1.0",END))
    textarea.config(state=DISABLED)
    textarea.see("end")
    writearea.delete("1.0",END)

start=Tk()

frame=Frame(start, height=500)
start.title("Web Chat++")

writearea=Text(height=5, width=50)
writearea.pack(side=BOTTOM)

sendbutton=Button(text="ENVIAR",bg="#128C7E",fg="white",command=sendText)
sendbutton.pack(side=BOTTOM)

textarea=Text(height=25, width=50)
textarea.pack()
scrollbar=Scrollbar()
textarea.pack(side=LEFT, fill=Y)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=textarea.yview)
textarea.config(yscrollcommand=scrollbar.set)
textarea.config(state=DISABLED)

start.bind("<Return>",sendText)
frame.pack()
start.mainloop()
