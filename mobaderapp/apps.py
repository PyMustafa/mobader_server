from django.apps import AppConfig


class MobaderappConfig(AppConfig):
    name = 'mobaderapp'

    def ready(self):
        import mobaderapp.signals
