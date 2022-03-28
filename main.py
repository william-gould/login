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
        lblInfo.grid(row=0, column=0, columnspan=2, sticky='nswe')

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

        submitBtn = ttk.Button(self, text='Login', command=lambda: log())
        submitBtn.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=5)

        registerB = ttk.Button(self, text='Register', command=lambda: controller.show_frame(register))
        registerB.grid(row=101, column=0, sticky='nesw', padx=(5, 0))

        resetBtn = ttk.Button(self, text='Reset Password')
        resetBtn.grid(row=101, column=1, sticky='nesw', padx=(3, 5))

        def log():
            usern = username.get()
            passw = password.get()
            print("Attempting login.")

            if usern != '':
                c = connection.cursor()
                search = c.execute("SELECT * FROM user_TBL where username=?", (usern,))
                for x in search:
                    if passw == x[1]:
                        messagebox.showinfo('Success', 'Login successful')
                        print("Logged in as {}".format(usern))

                    else:
                        messagebox.showerror("Error", "Invalid username or password.")
                        print("Logged failed as {}".format(usern))

                        connection.commit()
            else:
                messagebox.showerror("Error", 'Please enter a username and password.')
                print("Login failed (blank fields)")


class register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        lblInfo = tk.Label(self, font=('arial', 25, 'bold'), text='Register')
        lblInfo.grid(row=0, column=0, columnspan=2, sticky='nesw')

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

        submitBtn = ttk.Button(self, text='Register', command=lambda: reg())
        submitBtn.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=5)

        registerB = ttk.Button(self, text='Back', command=lambda: controller.show_frame(login))
        registerB.grid(row=101, column=0, sticky='nesw', padx=(5, 0))

        def isBlank(*args):
            x = 0
            while x == 0:
                for i in args:
                    if i == '':
                        return True
                        print("blank")
                        x = 1
                    else:
                        return False
                        print("Not blank")

        def createAcc(username, password):
            c = connection.cursor()
            c.execute("INSERT Into user_TBL (username,password) VALUES(?,?)",
                      (username, password,))
            connection.commit()

        def checkExist(username):
            c = connection.cursor()
            search = c.execute("SELECT * FROM user_TBL where username=?", (username,))
            for x in search:
                if x[0] == username:
                    return True

        def reg():
            usern = username.get()
            passw = password.get()

            if not isBlank(usern, passw):
                if not checkExist(usern):
                    createAcc(usern, passw)
                    messagebox.showinfo('Success', 'Account created')
                else:
                    messagebox.showerror('Error', 'Username is taken.')
            else:
                messagebox.showerror('Error', 'Please enter a username and password.')




app = Main()
app.mainloop()
