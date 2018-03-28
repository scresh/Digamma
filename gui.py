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


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Tor Scanner :: Digamma')
        self.geometry('600x400')
        self.configure(background=SHARK)
        self.resizable(False, False)

        Entry(self).grid(row=0, column=0)
        ShizarButton('Search', backend_function).grid(row=0, column=1)
        Entry(self).grid(row=1, column=0)
        ShizarButton('...', backend_function).grid(row=1, column=1)


class ShizarButton(Button):
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
