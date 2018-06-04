#!/usr/bin/python
from Tkinter import *
import tkFileDialog
import ttk

import time

from local_modules.tools import *


LARGE_FONT = ("Monoscape Regular", 8, "bold italic")
WHITE = '#FFFFFF'
ALOHA = '#26272E'
SHARK = '#1A1A1D'
ABBEY = '#4E4E50'
CROWN = '#6F2232'
MONARCH = '#950740'
SHIZAR = '#C3073F'


def change_path(input_field):
    path = get_default_path()
    title = "Select file"
    file_type = (("all files", "*.*"),)
    path = tkFileDialog.asksaveasfilename(initialdir=path, title=title, filetypes=file_type)
    if len(path) != 0:
        input_field.configure(state=NORMAL)
        input_field.delete(0, END)
        input_field.insert(0, path)
        input_field.configure(state=DISABLED)


def select_phrase(input_field):
    input_field.configure(state=NORMAL)


def select_harvest(input_field):
    input_field.configure(state=DISABLED)


class Switch(Radiobutton):
    def __init__(self, owner, **kw):
        Radiobutton.__init__(self, owner, **kw)
        self.configure(activebackground=ALOHA)
        self.configure(activeforeground=WHITE)
        self.configure(highlightcolor=SHARK)
        self.configure(selectcolor=SHARK)
        self.configure(background=ALOHA)
        self.configure(foreground=WHITE)
        self.configure(borderwidth=0)
        self.configure(highlightthickness=0)


class WhiteText(Label):
    def __init__(self, owner, text):
        Label.__init__(self, owner, text=text)
        self.configure(fg=WHITE)
        self.configure(bg=ALOHA)


class Separator(Label):
    def __init__(self, owner):
        Label.__init__(self, owner)
        self.configure(bg=ALOHA)


class LogViewer(Text):
    def __init__(self, owner):
        Text.__init__(self, owner)
        self.configure(background=SHARK)
        self.configure(foreground=SHIZAR)
        self.configure(highlightcolor=SHIZAR)
        self.configure(highlightthickness=1)
        self.configure(height=16)
        self.configure(width=96)
        self.configure(state=DISABLED)


class WhiteEntry(ttk.Entry):
    def __init__(self, owner, text='', state=NORMAL):
        ttk.Entry.__init__(self, owner)
        self.delete(0, END)
        self.insert(0, text)
        self.configure(state=state)


class ShizarButton(Button):
    def __init__(self, owner, text, **kw):
        Button.__init__(self, owner, **kw)
        self.configure(activebackground=MONARCH)
        self.configure(activeforeground=WHITE)
        self.configure(background=SHIZAR)
        self.configure(foreground=WHITE)
        self.configure(font=LARGE_FONT)
        self.configure(relief=GROOVE)
        self.configure(text=text)
        self.configure(padx=40)

        
        
class TabBar(ttk.Notebook):
    def __init__(self, owner):
        ttk.Notebook.__init__(self, owner)
        self.grid(row=1, column=0, columnspan=80, rowspan=59, sticky='NESW')


class Tab(Frame):
    def __init__(self, owner):
        Frame.__init__(self, owner)
        self.configure(background=ALOHA)


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Digamma :: Tor & IoT Scanner')
        self.geometry('818x444')
        # self.iconbitmap('favicon.ico')
        self.resizable(False, False)
        self.configure(background=SHARK)

        # Create tabs and them to bar
        tab_bar = TabBar(self)
        tor_tab = Tab(tab_bar)
        iot_tab = Tab(tab_bar)
        au_tab = Tab(tab_bar)
        set_tab = Tab(tab_bar)

        tab_bar.add(tor_tab, text='Tor Search')
        tab_bar.add(iot_tab, text='IoT Search')
        tab_bar.add(set_tab, text='Settings')
        tab_bar.add(au_tab, text='About us')

        # Tkinter variables
        mode = IntVar()
        mode.set(1)
        log = StringVar()

        # Create all objects
        top_left = Separator(tor_tab)
        bottom_right = Separator(tor_tab)
        phrase_text = WhiteText(tor_tab, 'Phrase to search:')
        phrase_input = WhiteEntry(tor_tab)
        run_button = ShizarButton(tor_tab, 'Start')
        mode_text = WhiteText(tor_tab, 'Select mode:')
        path_button = ShizarButton(tor_tab, '...')
        phrase_radio = Switch(tor_tab, text="Phrase", variable=mode, value=1)
        harvest_radio = Switch(tor_tab, text="Harvest", variable=mode, value=2)
        output_text = WhiteText(tor_tab, 'Output file path:')
        path_input = WhiteEntry(tor_tab, text=get_default_path(), state=DISABLED)
        log_viewer = LogViewer(tor_tab)
        status_text = WhiteText(tor_tab, 'Choose mode')

        # Configure objects
        run_button.configure(command=lambda: print_log(log_viewer, get_default_path()))
        path_button.configure(command=lambda: change_path(path_input))
        phrase_radio.configure(command=lambda: select_phrase(phrase_input))
        harvest_radio.configure(command=lambda: select_harvest(phrase_input))

        # Set location for all objects
        top_left.grid(row=0, column=0)
        phrase_text.grid(row=1, column=1, padx=16, sticky='sw')
        phrase_input.grid(row=2, column=1, columnspan=8, padx=16, sticky='ew')
        run_button.grid(row=2, column=9, columnspan=2, padx=2, sticky='new')
        output_text.grid(row=3, column=1, padx=16, sticky='sw')
        path_input.grid(row=4, column=1, columnspan=8, padx=16, sticky='ew')
        path_button.grid(row=4, column=9, columnspan=2, padx=2, sticky='new')
        mode_text.grid(row=2, column=11, padx=16, columnspan=2, sticky='nw')
        phrase_radio.grid(row=3, column=11, columnspan=2, padx=16, sticky='nw')
        harvest_radio.grid(row=4, column=11, columnspan=2, padx=16, sticky='nw')
        log_viewer.grid(row=5, column=1, columnspan=12, rowspan=8, padx=16, pady=10, sticky='nesw')
        status_text.grid(row=13, column=1, columnspan=12, sticky='new')
        bottom_right.grid(row=13, column=13)

        


app = Application()
app.mainloop()