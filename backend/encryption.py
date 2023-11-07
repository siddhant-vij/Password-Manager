import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def generateSalt() -> bytes:
    return os.urandom(16)


def hashMasterPassword(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def getFernetKey(password: str, salt: bytes) -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))


class EncryptionManager:
    def __init__(self, username: str, password: str, saltPath: str = 'resources/hashSalt', hashPasswordPath: str = 'data/masterHash'):
        self.username = username
        self.password = password
        self.salt = self.loadOrCreateSalt(saltPath)
        self.hashPasswordPath = hashPasswordPath
        self.fernet = getFernetKey(password, self.salt)

    def returnUsername(self):
        return self.username

    def loadOrCreateSalt(self, saltPath: str) -> bytes:
        try:
            with open(saltPath, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            salt = generateSalt()
            with open(saltPath, 'wb') as f:
                f.write(salt)
            return salt

    def saveHashedPassword(self):
        if not os.path.exists(self.hashPasswordPath) or os.path.getsize(self.hashPasswordPath) == 0:
            hashedPassword = hashMasterPassword(self.username+self.password, self.salt)
            with open(self.hashPasswordPath, 'wb') as f:
                f.write(hashedPassword)

    def loadHashedPassword(self) -> bytes:
        try:
            with open(self.hashPasswordPath, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError("Hashed password file not found.")

    def verifyUsername(self, enteredUsername: str) -> bool:
        return self.username == enteredUsername

    def verifyPassword(self, enteredUsername: str, enteredPassword: str) -> bool:
        storedHash = self.loadHashedPassword()
        newHash = hashMasterPassword(enteredUsername+enteredPassword, self.salt)
        return newHash == storedHash

    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())

    def decrypt(self, token: bytes) -> str:
        return self.fernet.decrypt(token).decode()
