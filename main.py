import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

connection = sqlite3.connect('login.db')


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title('Login')
        self.frames = {}
        for i in (login, register):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(login)

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()


class login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        lblInfo = tk.Label(self, font=('arial', 50, 'bold'), text='Login', fg='grey90', bd=1)
        lblInfo.pack(pady=10, padx=10)


class register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


app = Main()
app.mainloop()
