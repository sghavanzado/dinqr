# utils/api_helpers.py
import re

def validate_email(email: str) -> bool:
    """Valida el formato de un email"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Valida requisitos mínimos de contraseña"""
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def success_response(data=None, message="Operação realizada com sucesso"):
    """Retorna resposta de sucesso padronizada"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response

def error_response(message="Erro interno do servidor", details=None):
    """Retorna resposta de erro padronizada"""
    response = {
        'success': False,
        'error': message
    }
    if details is not None:
        response['details'] = details
    return response

def success_response(data=None, message="Operação realizada com sucesso"):
    """Retorna resposta de sucesso padronizada"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response

def error_response(message="Erro interno do servidor", details=None):
    """Retorna resposta de erro padronizada"""
    response = {
        'success': False,
        'error': message
    }
    if details is not None:
        response['details'] = details
    return response