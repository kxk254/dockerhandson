import csv
from django.core.management.base import BaseCommand
from solitonRE.models import テナント

#  py manage.py import_csv edX/redb/data/敷金保証金.csv edX/redb/data/売上.csv edX/redb/data/契約.csv edX/redb/data/テナント.csv edX/redb/data/保証会社.csv edX/redb/data/管理項目.csv edX/redb/data/支払先.csv edX/redb/data/ステータス.csv edX/redb/data/費用.csv
# py manage.py import_テナント --csv_file "C:\Users\konno\OneDrive - SCM\Dev\edX\redb\data\テナント.csv" 


class Command(BaseCommand):
    help = 'Import data from CSV file into テナント model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                テナントID = row.get('テナントID')
                テナント名 = row.get('テナント名')
                print(テナントID, テナント名)
                テナント.objects.create(
                            id=row['テナントID'],
                            テナント名=row['テナント名'],
                            テナント住所=row['テナント住所'],
                            テナント電話番号=row['テナント電話番号'],
                            テナント担当者名=row['テナント担当者名'],
                        )
                
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into テナント model'))