from Tkinter import *
# from PIL import Image, ImageTk
import time

LARGE_FONT = ("Trebuchet MS", 12, "bold italic")
WHITE = '#FFFFFF'
SHARK = '#1A1A1D'
ABBEY = '#4E4E50'
CROWN = '#6F2232'
MONARCH = '#950740'
SHIZAR = '#C3073F'


def backend_function():
    print 'Hejc!'


def view_his():
    print "historia "


def clear_his():
    print "clear"


def dream_team():
    print "team::"


def sel():
    selection = "You selected the option " + str(var.get())
    label.config(text=selection)


class Application(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Tor Scanner :: Digamma')
        self.geometry('800x600')
        self.resizable(False, False)
        self.configure(background='#F2DEE7')
        self.input()
        self.create_button_1()
        self.create_button_2()
        self.create_menu()
        self.create_entry1()
        self.create_entry2()

        var = IntVar()
        self.create_radio_button_1()
        self.create_radio_button_2()
        # zegar
        self.clock = Label(self, font=('digital-7', 20, 'bold'), bg='#F2DEE7')
        # self.clock.pack(fill=BOTH, expand=1)
        self.clock.grid(row=4, column=1)
        self.tick()

    #       self.showImg()
    #   self.create_photo()

    # def create_photo(self):
    #     self.img = ImageTk.PhotoImage(Image.open("True1.gif"))
    #     self.panel = Label(root, image=img)
    #     self.panel.pack(side="bottom", fill="both", expand="yes")

    #    def showImg(self):
    #        load = Image.open("logo.png")
    #        render = ImageTk.PhotoImage(load)

    # labels can be text or images
    #        img = Label(self, image=render)
    #        img.image = render
    #       img.place(x=0, y=0)
    def tick(self):
        s = time.strftime('%H:%M:%S')
        if s != self.clock["text"]:
            self.clock["text"] = s
        self.clock.after(200, self.tick)

    def print_text(self):
        for x in range(10):
            self.textbox.insert(END, self.entry_1.get())
            self.textbox.insert(END, "\n")

    def create_entry1(self):
        self.entry_1 = Entry(self, width=40, relief=GROOVE)

        # self.entry_1.pack(side=TOP)
        self.entry_1.grid(row=0, column=0)

    def create_entry2(self):
        entry_2 = Entry_2()
        # self.entry_2.pack()
        entry_2.grid(row=1, column=0)

    def input(self):
        # textbox=Text_1() #funkcja "print" sie jebie bo textbox nie jest globalna,
        self.sb_textbox = Scrollbar(self)
        self.textbox = Text(self, width=50, height=15)
        # self.textbox.pack(side=BOTTOM)
        self.sb_textbox.place(in_=self.textbox, relx=1., rely=0, relheight=1.)
        self.textbox.place(x=50, y=100)
        self.textbox.insert(END, "Hello ", ("h1"))
        self.sb_textbox.config(command=self.textbox.yview)
        self.textbox.grid(row=3, column=0, columnspan=2)

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
        button_1 = Button_1('Search', self.print_text)
        # button_1.pack()
        button_1.grid(row=0, column=1)

    def create_button_2(self):
        button_2 = Button_2('stop', backend_function)
        # button_2.pack()
        button_2.grid(row=1, column=1)

    def create_radio_button_1(self):
        rd_1 = RadioButton_1('opcja', backend_function)
        # rd_1.pack()
        rd_1.grid(row=0, column=2)

    def create_radio_button_2(self):
        rd_2 = RadioButton_2('opcja2', backend_function)
        # rd_2.pack()
        rd_2.grid(row=1, column=2)


class Text_1(Text):
    def __init__(self):
        Text.__init__(self)
        self.configure(width=60)
        self.configure(height=50)


class Entry_1(Entry):
    def __init__(self):
        Entry.__init__(self)
        # self.configure(background =color)
        # self.configure(borderwidth =) #szerokosc obramowania
        # self.configure(disabledbackground =text)
        # self.configure(disabledforeground =)#kolor teksty gdy kontrolka nieaktywna
        # self.configure(exportselection=)# gdy ustawione jest na True to zaznaczony tekst automatycznie jest kopiowany do systemowego schowka
        # self.configure(font=font)
        # self.configure(foreground =)#kolor tekstu
        # self.configure(justify =)#pozycjonowanie tekstu wewnatrz
        # self.configure(relief=RAISED) #styl obramowania
        # self.configure(selectforeground =)#kolor zaznaczaniego teksu
        # self.configure(state=) #stan kontrolki


class Entry_2(Entry):
    def __init__(self):
        Entry.__init__(self)
        # self.configure(background =color)
        # self.configure(borderwidth =) #szerokosc obramowania
        # self.configure(disabledbackground =text)
        # self.configure(disabledforeground =)#kolor teksty gdy kontrolka nieaktywna
        # self.configure(exportselection=)# gdy ustawione jest na True to zaznaczony tekst automatycznie jest kopiowany do systemowego schowka
        # self.configure(font=font)
        # self.configure(foreground =)#kolor tekstu
        # self.configure(justify =)#pozycjonowanie tekstu wewnatrz
        self.configure(relief=RAISED)  # styl obramowania
        # self.configure(selectforeground =)#kolor zaznaczaniego teksu
        self.configure(state=DISABLED)  # stan kontrolki
        self.configure(width=40)


class RadioButton_1(Radiobutton):
    def __init__(self, text, command):
        Radiobutton.__init__(self)
        self.configure(text=text)
        self.configure(command=command)
        self.configure(background='#F5AAC8')
        self.configure(height=1)
        self.configure(width=5)


class RadioButton_2(Radiobutton):
    def __init__(self, text, command):
        Radiobutton.__init__(self)
        self.configure(text=text)
        self.configure(command=command)
        self.configure(background='#F5AAC8')
        self.configure(height=1)
        self.configure(width=5)


class Button_1(Button):
    def __init__(self, text, command):
        Button.__init__(self)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background='#CD7794')
        self.configure(borderwidth=2)

        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(command=command)
        self.configure(relief=GROOVE)
        self.configure(text=text)
        self.configure(padx=20)
        self.configure(height=1)
        self.configure(width=5)
        # self.configure(state=)#stan przyciku


class Button_2(Button):
    def __init__(self, text, command):
        Button.__init__(self)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background='#CD7794')
        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(command=command)
        self.configure(relief=RIDGE)
        self.configure(text=text)
        self.configure(padx=20)
        self.configure(height=1)
        self.configure(width=5)

        # self.configure(state=)#stan przciksu


app = Application()
app.mainloop()
