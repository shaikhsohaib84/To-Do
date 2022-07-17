from django.apps import AppConfig


class TodoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_app'

    def ready(self):
        from jobs import update
        update.start()