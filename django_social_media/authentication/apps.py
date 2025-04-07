from django.apps import AppConfig

from django_social_media import authentication


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    

    def ready(self):
        return authentication.signals