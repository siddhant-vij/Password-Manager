import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Optional
from .dialogs import MasterPasswordDialog
from .passwordForms import AddNewPasswordForm, EditPasswordForm
from backend.passwordManager import PasswordStore
from backend.encryption import EncryptionManager
from backend.utilities import copyToClipboard, validateEmail


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Password Manager")
        self.passwordStore = None
        self.displayingEmails = False
        self.createWidgets()

    def createWidgets(self) -> None:
        # Search Bar
        self.searchVar = tk.StringVar()
        self.searchEntry = ttk.Entry(
            self, foreground='grey', textvariable=self.searchVar, width=40)
        self.searchEntry.grid(
            row=0, column=0, columnspan=2, padx=(10, 0), pady=10)
        self.searchEntry.insert(0, "Search the List...")
        placeholderText = self.searchEntry.get()
        def onEntryClick(event): return self.onEntryClick(placeholderText, event)
        def onFocusout(event): return self.onFocusout(placeholderText, event)
        self.searchEntry.bind('<FocusIn>', onEntryClick)
        self.searchEntry.bind('<FocusOut>', onFocusout)
        self.searchVar.trace_add('write', self.updateListbox)

        # Listbox and Scrollbar
        self.listbox = tk.Listbox(self, width=40)
        self.listbox.bind('<<ListboxSelect>>', self.onWebsiteSelect)
        self.listbox.grid(row=1, column=0, columnspan=3,
                          rowspan=4, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=3, sticky='ns', rowspan=4)

        # Create email buttons
        self.createEmailButtons()
    
    def onEntryClick(self, placeholderText, event):
        if self.searchEntry.get() == placeholderText:
            self.searchEntry.delete(0, tk.END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(foreground='black')

    def onFocusout(self, placeholderText, event):
        if self.searchEntry.get() == '':
            self.searchEntry.insert(0, placeholderText)
            self.searchEntry.config(foreground='grey')
            self.updateListbox()

    def newPassword(self) -> None:
        if self.displayingEmails and hasattr(self, 'selectedWebsite'):
            AddNewPasswordForm(
                self, self.passwordStore, prefillWebsite=self.selectedWebsite, saveCallback=self.updateListbox)
        else:
            AddNewPasswordForm(self, self.passwordStore,
                               saveCallback=self.updateListbox)
        self.addButton.focus_set()

    def updateListbox(self, *args, **kwargs) -> None:
        searchTerm = self.searchVar.get().lower()
        self.listbox.delete(0, tk.END)            
        if searchTerm == "search the list...":
            searchTerm = ""

        if self.displayingEmails:
            for email in sorted(self.passwordStore.getEmails(self.selectedWebsite)):
                if email.lower().startswith(searchTerm):
                    self.listbox.insert(tk.END, email)
        else:
            for website in sorted(self.passwordStore.passwords.keys()):
                if website.lower().startswith(searchTerm):
                    self.listbox.insert(tk.END, website)

    def onWebsiteSelect(self, event: Any) -> None:
        if not self.passwordStore:
            return
        self.clearButtons()
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.selectedWebsite = self.listbox.get(index)
            emails = sorted(self.passwordStore.getEmails(self.selectedWebsite))
            self.listbox.delete(0, tk.END)
            for email in emails:
                self.listbox.insert(tk.END, email)
            self.listbox.bind('<<ListboxSelect>>', self.onEmailSelect)
            self.goBackButton['state'] = 'normal'
            self.displayingEmails = True

    def createEmailButtons(self):
        self.addButton = ttk.Button(
            self, text="Add Password", command=self.newPassword, width=15)
        self.copyButton = ttk.Button(
            self, text="Copy Password", state='disabled', command=self.copyPassword, width=15)
        self.editButton = ttk.Button(
            self, text="Edit Password", state='disabled', command=self.editPassword, width=15)
        self.deleteButton = ttk.Button(
            self, text="Delete Password", state='disabled', command=self.deletePassword, width=15)
        self.goBackButton = ttk.Button(
            self, text="Go Back", state='disabled', command=self.goBack, width=15)

        self.addButton.grid(row=0, column=4, padx=10, pady=10)
        self.copyButton.grid(row=1, column=4, padx=5)
        self.editButton.grid(row=2, column=4, padx=5)
        self.deleteButton.grid(row=3, column=4, padx=5)
        self.goBackButton.grid(row=4, column=4, padx=5)

    def onEmailSelect(self, event: Any) -> None:
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.selectedEmail = self.listbox.get(index)
            self.copyButton['state'] = 'normal'
            self.editButton['state'] = 'normal'
            self.deleteButton['state'] = 'normal'
            self.goBackButton['state'] = 'normal'

    def copyPassword(self):
        password = self.passwordStore.getPassword(
            self.selectedWebsite, self.selectedEmail)
        copyToClipboard(password)

    def editPassword(self):
        password = self.passwordStore.getPassword(
            self.selectedWebsite, self.selectedEmail)
        EditPasswordForm(self, self.passwordStore, self.selectedWebsite,
                         self.selectedEmail, password, saveCallback=self.updateListbox)

    def deletePassword(self):
        if messagebox.askyesno("Confirm Delete", f"Delete password for {self.selectedEmail} at {self.selectedWebsite}?"):
            self.passwordStore.deletePassword(
                self.selectedWebsite, self.selectedEmail)
            self.listbox.delete(self.listbox.curselection()[0])
            self.clearButtons()

    def goBack(self):
        self.displayingEmails = False
        self.listbox.bind('<<ListboxSelect>>', self.onWebsiteSelect)
        self.listbox.delete(0, tk.END)
        if self.passwordStore:
            for website in sorted(self.passwordStore.passwords.keys()):
                self.listbox.insert(tk.END, website)
        self.clearButtons()
        self.goBackButton['state'] = 'disabled'

    def clearButtons(self):
        self.copyButton['state'] = 'disabled'
        self.editButton['state'] = 'disabled'
        self.deleteButton['state'] = 'disabled'

    def login(self):
        self.withdraw()
        mpd: MasterPasswordDialog = MasterPasswordDialog(self)
        try:
            masterUsername = mpd.result[0]
            masterPassword = mpd.result[1]
            self.encryptionManager: EncryptionManager = EncryptionManager(
                masterUsername, masterPassword)
            self.encryptionManager.saveHashedPassword()
            if self.encryptionManager.verifyPassword(masterUsername, masterPassword):
                self.deiconify()
                self.passwordStore = PasswordStore(self.encryptionManager)
                self.updateListbox()
                self.mainloop()
            else:
                messagebox.showerror(
                    "Error", "Incorrect Details. Try again or press Cancel.")
                self.login()
        except TypeError:
            messagebox.showinfo("Password Manager",
                                "Hope you have a great day ahead!")
