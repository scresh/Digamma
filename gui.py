# coding=utf-8
from Tkinter import *
#from tcl import n1

def backend_function():
    print 'Hej!'

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)

def zamknij(zdarzenie):
    for x in range(10):
        x=entry_1.get()
        print(x)
   # print(entry_1.get())
    okno.quit()
    okno.destroy()

def view_his():
    print "historia "

def clear_his():
    print "clear"

def dream_team():
    print "team::"

def wypisz(text):
    for x in range(10):
        textbox.insert(END,entry_1.get())
        textbox.insert(END,"\n")

okno = Tk()

topFrame=Frame(okno)
topFrame.pack()
buttonFrame=Frame(okno)
buttonFrame.pack()

etykieta = Label(topFrame, text="tu będzie zdjęcie!!oneone", font=("Arial", 24, "italic"),foreground="yellow", background="blue")
etykieta.grid(row=0,column=0,columnspan=2,pady=120)
#etykieta.pack(expand=NO,pady=100)

#photo = PhotoImage("n1.png")
#label_1=Label(topFrame,image=photo)
#label_1.grid(row=0,column=0,columnspan=2,pady=120)
#label_1.pack(pady=100)

entry_1=Entry(buttonFrame)
entry_1.grid(row=1,column=0)


button_1=Button(buttonFrame, text = "Search",font=("Courier",16,"bold"), background="red")
button_1.bind("<Button-1>", wypisz)
button_1.grid(row=1,column=1)
#przycisk_1.pack(side=LEFT)


#Drop down menu
menu=Menu(okno)
okno.config(menu=menu)

hisMenu=Menu(menu)
menu.add_cascade(label="History",menu=hisMenu)
hisMenu.add_command(label="View",command=view_his)
hisMenu.add_command(label="Clear",command=clear_his)

infoMenu=Menu(menu)
menu.add_cascade(label="Info",menu=infoMenu)
infoMenu.add_command(label="Team",command=dream_team)
#radiobutton
var = IntVar()
R1 = Radiobutton(buttonFrame, text="Option 1", variable=var, value=1, command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(buttonFrame, text="Option 2", variable=var, value=2, command=sel)
R2.pack( anchor = W )

#input
sb_textbox=Scrollbar(okno)
textbox=Text(okno,width=50,height=50)
textbox.pack(side=BOTTOM)
sb_textbox.place(in_=textbox,relx=1.,rely=0,relheight=1.)
#textbox.place(x=100,y=10)
textbox.insert(END,"Hello ",("h1"))
sb_textbox.config(command = textbox.yview)
okno.title("Digamma")
okno.mainloop()