from django.apps import AppConfig

class QuizConfig(AppConfig):
    name = 'witchquiz'

    def ready(self):
        from .scoreing import start

        start()

        from . import signals