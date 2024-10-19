from django.apps import AppConfig
from django.core.management import call_command


class SolitonreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solitonRE'

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # Trigger the backup every time the app is ready
        call_command('backup_db')