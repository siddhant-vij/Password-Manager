import string
import random
import re
import pyperclip
from typing import List
from urllib.parse import urlparse

LOWERCASE: str = string.ascii_lowercase
UPPERCASE: str = string.ascii_uppercase
DIGITS: str = string.digits
SPECIAL_CHARACTERS: str = "!@#$%^&*()-__+."

# Regex pattern for password validation
PASSWORD_PATTERN: re.Pattern = re.compile(r'^(?=(.*[a-z]){3,})(?=(.*[A-Z]){2,})(?=(.*[0-9]){2,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$')

def generateStrongPassword(length: int = 16) -> str:
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")
    password: List[str] = []
    password.extend(random.sample(LOWERCASE, 3))
    password.extend(random.sample(UPPERCASE, 2))
    password.extend(random.sample(DIGITS, 2))
    password.extend(random.sample(SPECIAL_CHARACTERS, 1))
    allCharacters: str = LOWERCASE + UPPERCASE + DIGITS + SPECIAL_CHARACTERS
    password.extend(random.choices(allCharacters, k=length - 8))
    random.shuffle(password)
    return ''.join(password)

def copyToClipboard(text: str) -> None:
    pyperclip.copy(text)

def shortenURLtoWebsiteName(url: str) -> str:
    secondLevelTlds = ['co.in', 'com.au', 'co.uk', 'org.uk', 'com.br', 'com.cn', 'co.jp', 'co.nz', 'co.za', 'com.sg', 'net.in', 'firm.in', 'gen.in', 'ind.in', 'net.au', 'org.au', 'org.cn', 'edu.in', 'res.in']
    if '.' not in url:
        url += '.com'
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    netloc = urlparse(url).netloc
    netloc = netloc.split(':')[0]
    parts = netloc.split('.')
    if len(parts) > 1 and '.'.join(parts[-2:]) in secondLevelTlds:
        primaryDomain = '.'.join(parts[-3:])
    elif len(parts) > 2 and '.'.join(parts[-3:]) in secondLevelTlds:
        primaryDomain = '.'.join(parts[-4:])
    else:
        primaryDomain = '.'.join(parts[-2:])
    return primaryDomain.lower()

def validateEmail(email: str) -> bool:
    pattern: re.Pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return pattern.match(email) is not None

def validatePassword(password: str) -> bool:
    return PASSWORD_PATTERN.match(password) is not None
