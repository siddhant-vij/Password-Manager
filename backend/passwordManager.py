import json
from typing import Dict, Optional
from .encryption import EncryptionManager

class PasswordStore:
    def __init__(self, encryptionManager: EncryptionManager):
        self.encryptionManager = encryptionManager
        self.dataPath = 'data/passwords.json.enc'
        self.passwords = self.loadPasswords()

    def loadPasswords(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self.dataPath, 'rb') as f:
                encryptedData = f.read()
            data = self.encryptionManager.decrypt(encryptedData)
            return json.loads(data)
        except FileNotFoundError:
            return {}

    def savePasswords(self):
        data = json.dumps(self.passwords, indent=4)
        encryptedData = self.encryptionManager.encrypt(data)
        with open(self.dataPath, 'wb') as f:
            f.write(encryptedData)

    def addPassword(self, website: str, email: str, password: str):
        if website not in self.passwords:
            self.passwords[website] = {}
        self.passwords[website][email] = password
        self.savePasswords()

    def getEmails(self, website: str) -> list[str]:
        return list(self.passwords.get(website, {}).keys())

    def getPassword(self, website: str, email: str) -> Optional[str]:
        return self.passwords.get(website, {}).get(email)

    def deletePassword(self, website: str, email: str) -> None:
        if website in self.passwords and email in self.passwords[website]:
            del self.passwords[website][email]
            if not self.passwords[website]:
                del self.passwords[website]
            self.savePasswords()

    def updatePassword(self, website: str, email: str, newPassword: str) -> None:
        if website in self.passwords and email in self.passwords[website]:
            self.passwords[website][email] = newPassword
            self.savePasswords()
    
    def updateEmail(self, website: str, oldEmail: str, newEmail: str) -> None:
        if website in self.passwords and oldEmail in self.passwords[website]:
            self.passwords[website][newEmail] = self.passwords[website][oldEmail]
            del self.passwords[website][oldEmail]
            self.savePasswords()

    def getPreFilledEmail(self) -> str:
        return self.encryptionManager.returnUsername()+'@gmail.com'
