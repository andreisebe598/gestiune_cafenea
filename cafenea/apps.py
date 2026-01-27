from django.apps import AppConfig


class CafeneaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafenea'

    def ready(self):
        import cafenea.signals  # type: ignore