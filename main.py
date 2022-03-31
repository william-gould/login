import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

connection = sqlite3.connect('login.db')


def checkExist(*args):
    c = connection.cursor()
    x = 0
    username1 = args[0]
    search = c.execute("SELECT * FROM user_TBL where username=?", (username1,))
    for z in search:
        if z[0] == username1:
            x = x + 1
        if z[2] == args[1]:
            x = x + 1
    return x


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title('Login')
        self.frames = {}
        for i in (login, register, reset):
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

        resetBtn = ttk.Button(self, text='Reset Password', command=lambda: controller.show_frame(reset))
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
        memInformation = StringVar()

        lblUser = tk.Label(self, text='Username: ', relief=RIDGE, width=10)
        lblUser.grid(row=3, column=0, sticky='w')
        txtUser = tk.Entry(self, textvariable=username, justify='left', relief=SUNKEN, width=15)
        txtUser.grid(row=3, column=1, sticky='w')

        lblPass = tk.Label(self, text='Password: ', relief=RIDGE, width=10)
        txtPass = tk.Entry(self, textvariable=password, justify='left', relief=SUNKEN, width=15)
        txtPass.config(show='*')
        lblPass.grid(row=4, column=0, sticky='w')
        txtPass.grid(row=4, column=1, sticky='w')

        lblMem = tk.Label(self, text='Test: ', relief=RIDGE, width=10)
        txtMem = tk.Entry(self, textvariable=memInformation, justify='left', relief=SUNKEN, width=15)
        lblMem.grid(row=5, column=0, sticky='w')
        txtMem.grid(row=5, column=1, sticky='w')

        submitBtn = ttk.Button(self, text='Register', command=lambda: reg())
        submitBtn.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=5)

        registerB = ttk.Button(self, text='Back', command=lambda: controller.show_frame(login))
        registerB.grid(row=101, column=0, sticky='nesw', padx=(5, 0))

        def isBlank(*args):
            x = 0
            for i in args:
                if i == '':
                    x = 1
                    print("blank")
                else:
                    print("Not blank")

            if x == 1:
                return True
            else:
                return False

        def createAcc(username, password, meminfo):
            c = connection.cursor()
            c.execute("INSERT Into user_TBL (username,password,information) VALUES(?,?,?)",
                      (username, password, meminfo,))
            connection.commit()

        def reg():
            usern = username.get()
            passw = password.get()
            meminf = memInformation.get()

            if not isBlank(usern, passw, meminf):
                if checkExist(usern) == 0:
                    createAcc(usern, passw, meminf)
                    messagebox.showinfo('Success', 'Account created')
                else:
                    messagebox.showerror('Error', 'Username is taken.')
            else:
                messagebox.showerror('Error', 'Please enter a username and password.')


class reset(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lblInfo = tk.Label(self, font=('arial', 25, 'bold'), text='Reset Password')
        lblInfo.grid(row=0, column=0, columnspan=2, sticky='nesw')

        username = StringVar()
        memInformation = StringVar()
        newPass = StringVar()

        lblUser = tk.Label(self, text='Username: ', relief=RIDGE, width=10)
        lblUser.grid(row=3, column=0, sticky='w')
        txtUser = tk.Entry(self, textvariable=username, justify='left', relief=SUNKEN, width=15)
        txtUser.grid(row=3, column=1, sticky='w')

        lblMem = tk.Label(self, text='Test: ', relief=RIDGE, width=10)
        txtMem = tk.Entry(self, textvariable=memInformation, justify='left', relief=SUNKEN, width=15)
        lblMem.grid(row=5, column=0, sticky='w')
        txtMem.grid(row=5, column=1, sticky='w')

        lblPass = tk.Label(self, text='New Password: ', relief=RIDGE, width=10)
        txtPass = tk.Entry(self, textvariable=newPass, justify='left', relief=SUNKEN, width=15)
        txtPass.config(show='*')
        lblPass.grid(row=4, column=0, sticky='w')
        txtPass.grid(row=4, column=1, sticky='w')

        submitBtn = ttk.Button(self, text='Register', command=lambda: resetPass())
        submitBtn.grid(row=100, column=0, columnspan=2, sticky='nesw', padx=5)

        registerB = ttk.Button(self, text='Back', command=lambda: controller.show_frame(login))
        registerB.grid(row=101, column=0, sticky='nesw', padx=(5, 0))

        def resetPass():
            usern = username.get()
            meminf = memInformation.get()
            newp = newPass.get()
            if checkExist(usern, meminf) == 2:
                print("username & meminfo correct")
                c = connection.cursor()
                c.execute("UPDATE user_TBL SET password=? WHERE username=?",
                          (newp,usern))

                connection.commit()
                messagebox.showinfo("LoginSys", "Successfully updated password for {}".format(usern))
            elif checkExist(usern, meminf) == 1:
                messagebox.showerror('Login Sys',"Incorrect memorable information")
            else:
                messagebox.showerror('Login Sys', 'User does not exist')


app = Main()
app.mainloop()
