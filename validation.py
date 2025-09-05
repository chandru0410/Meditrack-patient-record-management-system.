import re

def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_phone(phone: str) -> bool:
    return re.match(r"^\+?\d{10,15}$", phone) is not None
