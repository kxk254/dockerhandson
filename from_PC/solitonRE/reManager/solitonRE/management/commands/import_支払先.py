import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 支払先

# py manage.py import_支払先 --csv_file "C:\Users\konno\OneDrive - SCM\Dev\edX\redb\data\支払先.csv" 

class Command(BaseCommand):
    help = 'Import data from CSV file into 支払先 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                支払先.objects.create(
                    支払先コード=row['支払先コード'],
                    請求先名=row['請求先名'],
                    請求先住所=row['請求先住所'],
                    請求先担当者=row['請求先担当者'],
                    請求先電話番号=row['請求先電話番号'],
                )



        self.stdout.write(self.style.SUCCESS('Data imported successfully into 支払先 model'))


