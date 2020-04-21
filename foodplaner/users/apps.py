from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """
            - import recommended by Django Documentation:
                https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready
        """
        import users.signals
