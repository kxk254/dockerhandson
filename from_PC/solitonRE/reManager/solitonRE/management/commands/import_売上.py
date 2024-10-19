import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 売上

# py manage.py import_売上 --csv_file  "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/D_Rev816.csv" 

class Command(BaseCommand):
    help = 'Import data from CSV file into 売上 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Step 1: Delete existing data
        売上.objects.all().delete()

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                売上.objects.create(
                    物件ID_id=row['物件ID'],#
                    テナントID_id=row['テナントID'],#
                    管理項目コード_id=row['管理項目コード'],#
                    契約ID_id=row['契約ID'],#
                    レポート日=row['レポート日'],#
                    該当月開始月=row['該当月開始月'],#
                    該当月終了月=row['該当月終了月'],#
                    請求書発行日=row['請求書発行日'],#
                    入金予定日=row['入金予定日'],#
                    計上日=row['計上日'],#
                    請求金額=row['請求金額'],#
                    請求消費税=row['請求消費税'],#
                    請求税込金額=row['請求税込金額'],#
                    当月入金日=row['当月入金日'],#
                    備考=row['備考'],#
                    DeleteFlag=row['DeleteFlag'],#
                )
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into 売上 model'))