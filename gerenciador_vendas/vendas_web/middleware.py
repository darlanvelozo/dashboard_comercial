import re

from django.conf import settings
from django.shortcuts import redirect


_EXEMPT_PATTERNS = [
    re.compile(r"^admin/login/?$"),
    re.compile(r"^admin/logout/?$"),
    re.compile(r"^admin/password_reset/"),
    re.compile(r"^static/"),
    re.compile(r"^favicon\.ico$"),
    # APIs não devem requerer autenticação
    re.compile(r"^api/"),
]


class LoginRequiredMiddleware:
    """Middleware que força autenticação nas páginas do painel.

    Exceções: página de login do admin, logout, reset de senha, arquivos estáticos, favicon e APIs.
    Redireciona para settings.LOGIN_URL com parâmetro next.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_no_slash = request.path.lstrip('/')

        # Sempre permitir as URLs isentas
        for pattern in _EXEMPT_PATTERNS:
            if pattern.match(path_no_slash):
                return self.get_response(request)

        # Se já autenticado, libera
        if request.user.is_authenticated:
            return self.get_response(request)

        # Redireciona para login do admin por padrão
        login_url = getattr(settings, 'LOGIN_URL', '/admin/login/')
        return redirect(f"{login_url}?next={request.path}")


