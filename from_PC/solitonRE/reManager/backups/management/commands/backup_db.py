import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Backup the SQLite database'

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        backup_path = os.path.join(settings.BASE_DIR, 'db_backup.sqlite3')
        shutil.copyfile(db_path, backup_path)
        self.stdout.write(self.style.SUCCESS('Database backup created successfully'))