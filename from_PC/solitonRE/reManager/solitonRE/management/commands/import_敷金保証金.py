import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 敷金保証金

# py manage.py import_敷金保証金 --csv_file  "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/敷金保証金.csv" 

class Command(BaseCommand):
    help = 'Import data from CSV file into 敷金保証金 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                敷金保証金.objects.create(
                    契約番号_id=row['契約番号'],
                    テナントID_id=row['テナントID'],
                    契約区画=row['契約区画'],
                    定借区分=row['定借区分'],
                    種類=row['種類'],
                    前月末残高=row['前月末残高'],
                    当月増額=row['当月増額'],
                    当月減少=row['当月減少'],
                    今月末残高=row['今月末残高'],
                    移動予定日=row['移動予定日'] if row['移動予定日'] else None,
                    保証会社コード_id=row['保証会社コード'],
                    DeleteFlag=row['DeleteFlag']
                )
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into 敷金保証金 model'))