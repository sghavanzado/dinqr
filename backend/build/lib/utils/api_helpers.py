# utils/api_helpers.py
import re

def validate_email(email: str) -> bool:
    """Valida el formato de un email"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Valida requisitos mínimos de contraseña"""
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)