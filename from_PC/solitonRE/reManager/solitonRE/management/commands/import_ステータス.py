import csv
from django.core.management.base import BaseCommand
from solitonRE.models import ステータス

# py manage.py import_ステータス --csv_file  "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/ステータス.csv" 

class Command(BaseCommand):
    help = 'Import data from CSV file into ステータス model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                ステータス.objects.create(
                    レポート日=row['レポート日'],
                    新テナント=row['新テナント'],
                    テナント関連=row['テナント関連'],
                    遅延状況=row['遅延状況'],
                    検査情報=row['検査情報'],
                    メンテナンス=row['メンテナンス'],
                    その他=row['その他'],
                    特別項目=row['特別項目'],
                    DeleteFlag=row['DeleteFlag'],
                )
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into ステータス model'))