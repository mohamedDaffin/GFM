from django.apps import AppConfig


class AnimaleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animaleapp'
    def ready(self):
        import animaleapp.signals
