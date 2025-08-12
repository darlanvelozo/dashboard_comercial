from django.apps import AppConfig


class VendasWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendas_web'

    def ready(self):
        # Registrar sinais do app
        from . import signals  # noqa: F401
