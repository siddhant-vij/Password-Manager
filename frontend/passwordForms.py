import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable, Optional

from backend.passwordManager import PasswordStore
from backend.utilities import generateStrongPassword, validatePassword, copyToClipboard, shortenURLtoWebsiteName, validateEmail


class FormBase(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        passwordStore: PasswordStore,
        title: str,
        website: str = '',
        email: str = '',
        password: str = '',
        saveCallback: Optional[Callable] = None
    ) -> None:
        super().__init__(parent)
        self.title(title)
        self.passwordStore: PasswordStore = passwordStore
        self.website: str = website
        self.email: str = email
        self.password: str = password
        self.createWidgets()
        self.transient(parent)
        self.grab_set()
        self.saveCallback = saveCallback

    def createWidgets(self) -> None:
        style = ttk.Style(self)
        style.configure('Save.TButton', background='green')
        self.siteVar: tk.StringVar = tk.StringVar()
        self.emailVar: tk.StringVar = tk.StringVar()
        self.passwordVar: tk.StringVar = tk.StringVar()
        self.createLabelsAndEntries()
        self.createButtons()
        self.siteVar.trace_add('write', lambda *args: self.onFieldChange())
        self.emailVar.trace_add('write', lambda *args: self.onFieldChange())
        self.passwordVar.trace_add('write', lambda *args: self.onFieldChange())

    def createLabelsAndEntries(self) -> None:
        raise NotImplementedError(
            "Subclasses must implement createLabelsAndEntries")

    def createButtons(self) -> None:
        self.generateButton: ttk.Button = ttk.Button(
            self, text="Generate", command=self.generatePassword)
        self.generateButton.grid(row=5, column=1, padx=(10, 10))

        self.saveButton: ttk.Button = ttk.Button(
            self, text="Save", state='disabled', command=self.savePassword)
        self.saveButton.grid(row=6, column=1, pady=(
            30, 15), padx=10, sticky='e')

        self.cancelButton: ttk.Button = ttk.Button(
            self, text="Cancel", command=self.destroy)
        self.cancelButton.grid(
            row=6, column=0, pady=(30, 15), padx=5, sticky='e')

    def onFieldChange(self) -> None:
        if (self.websiteEntry.get() and self.emailEntry.get() and self.passwordEntry.get()):
            self.saveButton['state'] = 'normal'
            self.saveButton['style'] = 'Save.TButton'
        else:
            self.saveButton['state'] = 'disabled'
            self.saveButton['style'] = ''

    def generatePassword(self) -> None:
        password: str = generateStrongPassword()
        self.passwordEntry.delete(0, tk.END)
        self.passwordEntry.insert(0, password)
        copyToClipboard(password)

    def savePassword(self) -> None:
        website: str = shortenURLtoWebsiteName(self.websiteEntry.get())
        email: str = self.emailEntry.get()
        password: str = self.passwordEntry.get()

        if not validateEmail(email):
            messagebox.showerror(
                "Error", "Email does not meet validation criteria.")
            return

        if not validatePassword(password):
            messagebox.showerror("Error", "Password does not meet criteria.")
            return

        if website and email and password:
            self.passwordStore.addPassword(website, email, password)
            if self.saveCallback:
                self.saveCallback()
            self.destroy()


class AddNewPasswordForm(FormBase):
    def __init__(
            self,
            parent: tk.Tk,
            passwordStore: PasswordStore,
            prefillWebsite: str = '',
            saveCallback: Optional[Callable] = None
        ) -> None:
        super().__init__(parent, passwordStore, "Add New Password", website=prefillWebsite, saveCallback=saveCallback)
        self.saveCallback = saveCallback

    def createLabelsAndEntries(self) -> None:
        siteLabel = ttk.Label(self, text="Website:")
        siteLabel.grid(row=0, column=0, sticky='w', pady=(15, 5))
        siteLabel.config(padding=(10, 0))
        self.websiteEntry = ttk.Entry(
            self, textvariable=self.siteVar, width=34)
        self.websiteEntry.grid(
            row=1, column=0, columnspan=2, pady=5, padx=(10, 10))

        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=2, column=0, sticky='w', pady=(20, 5))
        emailLabel.config(padding=(10, 0))
        self.emailEntry = ttk.Entry(self, textvariable=self.emailVar, width=34)
        self.emailEntry.grid(row=3, column=0, columnspan=2,
                             pady=5, padx=(10, 10))
        self.emailEntry.insert(0, self.passwordStore.getPreFilledEmail())
        if self.website:
            self.websiteEntry.insert(0, self.website)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=4, column=0, sticky='w', pady=(20, 5))
        passwordLabel.config(padding=(10, 0))
        self.passwordEntry = ttk.Entry(
            self, textvariable=self.passwordVar, show='*')
        self.passwordEntry.grid(row=5, column=0, pady=5, padx=(10, 0))


class EditPasswordForm(FormBase):
    def __init__(
        self,
        parent: tk.Tk,
        passwordStore: PasswordStore,
        website: str,
        email: str,
        password: str,
        saveCallback: Optional[Callable] = None
    ) -> None:
        super().__init__(parent, passwordStore, "Edit Password", website, email, password, saveCallback)
        self.website = website
        self.email = email
        self.password = password
        self.saveCallback = saveCallback

    def createLabelsAndEntries(self) -> None:
        siteLabel = ttk.Label(self, text="Website:")
        siteLabel.grid(row=0, column=0, sticky='w', pady=(15, 5))
        siteLabel.config(padding=(10, 0))
        self.websiteEntry = ttk.Entry(
            self, textvariable=self.siteVar, width=34)
        self.websiteEntry.grid(
            row=1, column=0, columnspan=2, pady=5, padx=(10, 10))
        self.websiteEntry.insert(0, self.website)
        self.websiteEntry.config(state='readonly')

        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=2, column=0, sticky='w', pady=(20, 5))
        emailLabel.config(padding=(10, 0))
        self.emailEntry = ttk.Entry(self, textvariable=self.emailVar, width=34)
        self.emailEntry.grid(row=3, column=0, columnspan=2,
                             pady=5, padx=(10, 10))
        self.emailEntry.insert(0, self.email)
        self.emailEntry.config(state='readonly')

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=4, column=0, sticky='w', pady=(20, 5))
        passwordLabel.config(padding=(10, 0))
        self.passwordEntry = ttk.Entry(
            self, textvariable=self.passwordVar, show='*')
        self.passwordEntry.grid(row=5, column=0, pady=5, padx=(10, 0))
        self.passwordEntry.insert(0, self.password)
