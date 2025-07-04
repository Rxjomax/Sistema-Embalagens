# Ficheiro: logs/utils.py
from .middleware import RequestMiddleware

def get_current_user():
    """Retorna o usuário logado atualmente."""
    return RequestMiddleware.get_user()