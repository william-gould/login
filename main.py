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
        lblInfo = tk.Label(self, font=('arial', 25, 'bold'), text='Login', fg='grey90', bd=1)
        lblInfo.grid(row=0, column=0, columnspan=1, sticky='we')

        username = StringVar()
        password = StringVar()

        lblUser = tk.Label(self, text='Username: ', relief=RIDGE, width=10)
        lblUser.grid(row=3, column=0, sticky='w')
        txtUser = tk.Entry(self, textvariable=username, justify='left', relief=SUNKEN, width=15)
        txtUser.grid(row=3, column=1, sticky='w')

        lblPass = tk.Label(self, text='Password: ', relief=RIDGE, width=10)
        txtPass = tk.Entry(self, textvariable=password, justify='left', relief=SUNKEN, width=15)
        txtPass.config(show='*')
        lblPass.grid(row=4, column=0, sticky='w')
        txtPass.grid(row=4, column=1, sticky='w')

        submitBtn = ttk.Button(self, text='Login', command=lambda: log(username, password))
        submitBtn.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=5)

        registerB = ttk.Button(self, text='Register')
        registerB.grid(row=101, column=0, sticky='nesw', padx=(5,0))

        resetBtn = ttk.Button(self, text='Reset Password')
        resetBtn.grid(row=101, column=1, sticky='nesw', padx=(3,5))

        def log(user, password):
            usern = username.get()
            passw = password.get()

            if usern != '':
                c = connection.cursor()
                search = c.execute("SELECT * FROM user_TBL where username=?", (usern,))
                for x in search:
                    if passw == x[1]:
                        messagebox.showinfo('Success', 'Login successful')

                    else:
                        messagebox.showerror("Error", "Invalid username or password.")

                        connection.commit()
            else:
                messagebox.showerror("Error", 'Please enter a username and password.')


class register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        lblInfo = tk.Label(self, text='hello')


app = Main()
app.mainloop()
