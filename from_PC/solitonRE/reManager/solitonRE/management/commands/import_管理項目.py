import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 管理項目

#  py manage.py import_csv edX/redb/data/敷金保証金.csv edX/redb/data/売上.csv edX/redb/data/契約.csv edX/redb/data/管理項目.csv edX/redb/data/保証会社.csv edX/redb/data/管理項目.csv edX/redb/data/支払先.csv edX/redb/data/ステータス.csv edX/redb/data/費用.csv
# py manage.py import_管理項目 --csv_file "C:\Users\konno\OneDrive - SCM\Dev\edX\redb\data\管理項目.csv" 


class Command(BaseCommand):
    help = 'Import data from CSV file into 管理項目 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                管理項目.objects.create(
                    管理項目コード=row['管理項目コード'],
                    管理項目印字名=row['管理項目印字名'],
                    管理項目レポート分類区分=row['管理項目レポート分類区分'],
                )
                
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into 管理項目 model'))