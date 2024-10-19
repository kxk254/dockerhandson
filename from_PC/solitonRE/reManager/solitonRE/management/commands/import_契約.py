import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 契約

#  py manage.py import_csv edX/redb/data/敷金保証金.csv edX/redb/data/売上.csv edX/redb/data/契約.csv edX/redb/data/契約.csv edX/redb/data/保証会社.csv edX/redb/data/契約.csv edX/redb/data/支払先.csv edX/redb/data/ステータス.csv edX/redb/data/費用.csv
# py manage.py import_契約 --csv_file "C:\Users\konno\OneDrive - SCM\Dev\edX\redb\data\契約.csv" 


class Command(BaseCommand):
    help = 'Import data from CSV file into 契約 model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:

                契約.objects.create(
                    契約ID=row['契約ID'],
                    テナントID_id=row['テナントID'],
                    物件ID_id=row['物件ID'],
                    契約日=row['契約日'],
                    当初開始日=row['当初開始日'],
                    当初終了日=row['当初終了日'],
                    現在契約開始日=row['現在契約開始日'],
                    現在契約終了日=row['現在契約終了日'],
                    賃料金額=row['賃料金額'],
                    共益費=row['共益費'],
                    契約種類=row['契約種類'],
                    自動更新=row['自動更新'],
                    契約年数=row['契約年数'],
                    更新料有無=row['更新料有無'],
                    更新料金額=row['更新料金額'],
                    解約通知期間=row['解約通知期間'],
                    居室タイプ=row['居室タイプ'],
                    平米数=row['平米数'],
                    坪数=row['坪数'],
                    保証金金額=row['保証金金額'],
                    保証金月数=row['保証金月数'],
                    保証有無=row['保証有無'],
                    保証会社コード_id=row['保証会社コード'],
                    フリーレント=row['フリーレント'],
                    備考=row['備考'],
                )
                
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully into 契約 model'))