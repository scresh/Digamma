from Tkinter import *

LARGE_FONT = ("Trebuchet MS", 12, "bold italic")
WHITE = '#FFFFFF'
SHARK = '#1A1A1D'
ABBEY = '#4E4E50'
CROWN = '#6F2232'
MONARCH = '#950740'
SHIZAR = '#C3073F'

def backend_function():
    print 'Hej!'

def view_his():
    print "historia "

def clear_his():
    print "clear"

def dream_team():
    print "team::"

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)

class Application(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Tor Scanner :: Digamma')
        self.geometry('400x200')
        self.configure(background=SHARK)
        self.input()
        self.create_button_1()
        self.create_button_2()
        self.create_menu()
        self.create_entry1()
        self.create_entry2()

        var = IntVar()
        self.create_radio_button_1()
        self.create_radio_button_2()


    def print_text(self):
        for x in range(10):
            self.textbox.insert(END, self.entry_1.get())
            self.textbox.insert(END, "\n")

    def create_entry1(self):
        self.entry_1=Entry(self)
        #self.entry_1.pack(side=TOP)
        self.entry_1.grid(row=0,column=0)

    def create_entry2(self):
        self.entry_2 = Entry(self)
        #self.entry_2.pack()
        self.entry_2.grid(row=1,column=0)
    def input(self):
        self.sb_textbox=Scrollbar(self)
        self.textbox=Text(self, width=50, height=50)
        self.textbox.pack(side=BOTTOM)
        self.sb_textbox.place(in_=self.textbox, relx=1., rely=0, relheight=1.)
        self.textbox.place(x=100,y=10)
        self.textbox.insert(END, "Hello ", ("h1"))
        self.sb_textbox.config(command=self.textbox.yview)

    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        hisMenu = Menu(menu)
        menu.add_cascade(label="History", menu=hisMenu)
        hisMenu.add_command(label="View", command=view_his)
        hisMenu.add_command(label="Clear", command=clear_his)

        infoMenu = Menu(menu)
        menu.add_cascade(label="Info", menu=infoMenu)
        infoMenu.add_command(label="Team", command=dream_team)

    def create_button_1(self):
        button_1 = Button_1('Search',self.print_text)
        button_1.pack()


    def create_button_2(self):
        button_2=Button_2('stop',backend_function)
        button_2.pack()

    def create_radio_button_1(self):
        rd_1=RadioButton_1('opcja',backend_function)
        rd_1.pack()

    def create_radio_button_2(self):
        rd_2=RadioButton_1('opcja',backend_function)
        rd_2.pack()
class RadioButton_1(Radiobutton):
    def __init__(self,text,command):
        Radiobutton.__init__(self)
        self.configure(text=text)
        self.configure(command=command)

class RadioButton_2(Radiobutton):
    def __init__(self,text,command):
        Radiobutton.__init__(self)
        self.configure(text=text)
        self.configure(command=command)

class Button_1(Button):
    def __init__(self, text, command):
        Button.__init__(self)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background=SHIZAR)
        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(command=command)
        self.configure(relief=GROOVE)
        self.configure(text=text)
        self.configure(padx=20)

class Button_2(Button):
    def __init__(self, text, command):
        Button.__init__(self)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background=SHIZAR)
        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(command=command)
        self.configure(relief=GROOVE)
        self.configure(text=text)
        self.configure(padx=20)



app = Application()
app.mainloop()
