#!/usr/bin/python
from Tkinter import *
import ttk

LARGE_FONT = ("Trebuchet MS", 8, "bold italic")
WHITE = '#FFFFFF'
SHARK = '#1A1A1D'
ABBEY = '#4E4E50'
CROWN = '#6F2232'
MONARCH = '#950740'
SHIZAR = '#C3073F'


class Empty(Label):
    def __init__(self, owner):
        Label.__init__(self, owner)


class LogViewer(Text):
    def __init__(self, owner):
        Text.__init__(self, owner)
        self.configure(background=SHARK)
        self.configure(foreground=WHITE)
        self.configure(highlightcolor=SHIZAR)
        self.configure(height=16)
        self.configure(width=96)


class WhiteEntry(Entry):
    def __init__(self, owner):
        Entry.__init__(self, owner)


class ShizarButton(Button):
    def __init__(self, owner, text, command):
        Button.__init__(self, owner)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background=SHIZAR)
        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(command=command)
        self.configure(relief=GROOVE)
        self.configure(text=text)
        self.configure(padx=20)


class TabBar(ttk.Notebook):
    def __init__(self, owner):
        ttk.Notebook.__init__(self, owner)
        self.grid(row=1, column=0, columnspan=80, rowspan=59, sticky='NESW')


class Tab(Frame):
    def __init__(self, owner):
        Frame.__init__(self, owner)
        self.configure(background=SHARK)


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Tor Scanner :: Digamma')
        self.geometry('800x600')
        self.resizable(False, False)
        self.configure(background=SHARK)

        for r in xrange(60):
            self.rowconfigure(r, weight=1)
            self.columnconfigure(r, weight=1)

        tab_bar = TabBar(self)

        tor_tab = Tab(tab_bar)
        iot_tab = Tab(tab_bar)
        au_tab = Tab(tab_bar)
        set_tab = Tab(tab_bar)

        tab_bar.add(tor_tab, text='Tor Search')
        tab_bar.add(iot_tab, text='IoT Search')
        tab_bar.add(set_tab, text='Settings')
        tab_bar.add(au_tab, text='About us')

        # Tor Panel
        Empty(tor_tab).grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        Empty(tor_tab).grid(row=4, column=10, columnspan=10, padx=10, pady=10)

        WhiteEntry(tor_tab).grid(row=0, column=0, columnspan=3, padx=10, pady=0, sticky='we')
        ShizarButton(tor_tab, 'Start', None).grid(row=0, column=3, padx=10, pady=10, sticky='we')

        WhiteEntry(tor_tab).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='we')
        ShizarButton(tor_tab, '...', None).grid(row=1, column=3, padx=10, pady=10, sticky='we')

        LogViewer(tor_tab).grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        tor_tab.grid_columnconfigure(0, weight=1)


app = Application()
app.mainloop()
