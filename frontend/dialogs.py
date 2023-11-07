import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from typing import Optional, Tuple

from backend.utilities import validatePassword


class MasterPasswordDialog(simpledialog.Dialog):
    def __init__(self, parent: tk.Tk) -> None:
        self.result: Optional[Tuple[str, str]] = None
        self.username: str = ""
        self.password: str = ""
        self.usernameEntry: tk.Entry = None
        self.passwordEntry: tk.Entry = None
        super().__init__(parent, title="Master Password")

    def body(self, master: tk.Widget) -> tk.Entry:
        headerText: str = ("Password Manager is trying to show passwords. Type in your username and "
                           "master password to allow for this.")
        header: tk.Label = tk.Label(master, text=headerText, wraplength=300)
        header.grid(row=0, columnspan=2)
        header.config(padx=20, pady=10)

        usernameLabel: tk.Label = tk.Label(master, text="Username:")
        usernameLabel.grid(row=1)
        self.usernameEntry = tk.Entry(master)
        self.usernameEntry.grid(row=1, column=1)
        usernameLabel.config(padx=5, pady=5)

        passwordLabel: tk.Label = tk.Label(master, text="Password:")
        passwordLabel.grid(row=2)
        self.passwordEntry = tk.Entry(master, show='*')
        self.passwordEntry.grid(row=2, column=1)
        passwordLabel.config(padx=5, pady=5)

        return self.usernameEntry  # The widget to be focused initially

    def validate(self) -> bool:
        if not self.usernameEntry.get() and not self.passwordEntry.get():
            messagebox.showwarning("Invalid Input", "Username & Password cannot be empty.")
            return False
        if not self.usernameEntry.get():
            messagebox.showwarning("Invalid Input", "Username cannot be empty.")
            return False
        if not self.passwordEntry.get():
            messagebox.showwarning("Invalid Input", "Password cannot be empty.")
            return False
        if not validatePassword(self.passwordEntry.get()):
            messagebox.showwarning("Invalid Input", "Password does not meet criteria.")
            return False
        return True

    def apply(self) -> None:
        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        self.result = (self.username, self.password)
