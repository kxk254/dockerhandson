import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 保証会社

# py manage.py import_保証会社 --csv_file "C:\Users\konno\OneDrive - SCM\Dev\edX\redb\data\保証会社.csv" 


class Command(BaseCommand):
    help = 'Import data from CSV file into 保証会社 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                保証会社.objects.create(
                    保証会社コード=row['保証会社コード'],
                    保証会社名=row['保証会社名'],
                    保証会社住所=row['保証会社住所'],
                    保証会社担当者名=row['保証会社担当者名'],
                    保証会社連絡先=row['保証会社連絡先'],
                )
                
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into 保証会社 model'))