import csv
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import Model

import View


class LoginScreen(tk.Tk):

    def __init__(self):
        super().__init__()
        self.sv_ttk = None
        self.title("POS-System Login")
        self.center_window()

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="EW")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky="EW")

    def center_window(self):
        window_width = 340
        window_height = 150

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()


        if self.authenticate_user(username, password):
            self.destroy()
            messagebox.showinfo("Login Successful", "Welcome, admin!")
            app = View.Application()
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    @staticmethod
    def authenticate_user(username, password):

        with open(Model.USERS_FILE_PATH, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == username and row[1] == password:
                    return True
        return False



