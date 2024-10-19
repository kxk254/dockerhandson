import csv
from django.core.management.base import BaseCommand
from solitonRE.models import 敷金保証金, 売上, 契約, テナント, 保証会社, 管理項目, 支払先,  ステータス, 費用

#  py manage.py import_csv edX/redb/data/敷金保証金.csv edX/redb/data/売上.csv edX/redb/data/契約.csv edX/redb/data/テナント.csv edX/redb/data/保証会社.csv edX/redb/data/管理項目.csv edX/redb/data/支払先.csv edX/redb/data/ステータス.csv edX/redb/data/費用.csv
# py manage.py import_csv --csv_files "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/敷金保証金.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/売上.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/契約.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/テナント.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/保証会社.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/管理項目.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/支払先.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/ステータス.csv" "C:/Users/konno/OneDrive - SCM/Dev/edX/redb/data/費用.csv"

class Command(BaseCommand):
    help = 'Import data from CSV file into multiple  model'

    def add_arguments(self, parser):
        parser.add_argument('--csv_files', nargs='+', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_files = kwargs['csv_files']

        for csv_file in csv_files:
            model_name = csv_file.split('/')[-1].split('.')[0]

            with open(csv_file, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if model_name == '敷金保証金':
                    for row in reader:
                        敷金保証金.objects.create(
                            契約番号_id=row['契約番号'],
                            テナントID_id=row['テナントID'],
                            契約区画=row['契約区画'],
                            定借区分=row['定借区分'],
                            種類=row['種類'],
                            前月末残高=row['前月末残高'],
                            当月増額=row.get('当月増額') or 0,
                            当月減少=row.get('当月減少') or 0,
                            今月末残高=row['今月末残高'],
                            移動予定日=row['移動予定日'] if row['移動予定日'] else None,
                            保証会社コード_id=row['保証会社コード'],
                            DeleteFlag=row['DeleteFlag'].lower() in ('true', '1')
                        )

                elif model_name == '売上':    
                        # Import data into 売上 model
                        売上.objects.create(
                            物件ID_id=row['物件ID'],
                            テナントID_id=row['テナントID'],
                            管理項目コード_id=row['管理項目コード'],
                            契約番号_id=row['契約番号'],
                            レポート日=row['レポート日'],
                            該当月開始月=row['該当月開始月'],
                            該当月終了月=row['該当月終了月'],
                            請求書発行月=row['請求書発行月'],
                            入金予定日=row['入金予定日'],
                            計上日=row['計上日'],
                            請求金額=row['請求金額'],
                            請求消費税=row['請求消費税'],
                            請求税金込=row['請求税金込'],
                            当月入金額=row['当月入金額'],
                            備考=row.get('備考', ''),
                            DeleteFlag=row['DeleteFlag'].lower() in ('true', '1')
                        )
                
                elif model_name == '契約':    
                        # Import data into 売上 model
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
                            保証会社コード=row['保証会社コード'],
                            フリーレント=row['フリーレント'],
                            備考=row.get('備考', ''),
                        )
                elif model_name == 'テナント':    
                        # Import data into 売上 model
                        テナント.objects.create(
                            テナントID=row['テナントID'],
                            テナント名=row['テナント名'],
                            テナント住所=row['テナント住所'],
                            テナント電話番号=row['テナント電話番号'],
                            テナント担当者名=row['テナント担当者名'],
                        )
                
                elif model_name == '保証会社':    
                        # Import data into 売上 model
                        保証会社.objects.create(
                            保証会社コード=row['保証会社コード'],
                            保証会社名=row['保証会社名'],
                            保証会社住所=row['保証会社住所'],
                            保証会社担当者名=row['保証会社担当者名'],
                            保証会社連絡先=row['保証会社連絡先'],
                        )
                
                elif model_name == '管理項目':    
                        # Import data into 売上 model
                        管理項目.objects.create(
                            管理項目コード=row['管理項目コード'],
                            管理項目印字名=row['管理項目印字名'],
                            管理項目レポート分類区分=row['管理項目レポート分類区分'],
                        )
                
                elif model_name == '支払先':    
                        # Import data into 売上 model
                        支払先.objects.create(
                            支払先コード=row['支払先コード'],
                            請求先名=row['請求先名'],
                            請求先住所=row['請求先住所'],
                            請求先担当者=row['請求先担当者'],
                            請求先電話番号=row['請求先電話番号'],
                        )
                
                elif model_name == 'ステータス':    
                        # Import data into 売上 model
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

                elif model_name == '費用':    
                        # Import data into 売上 model
                        費用.objects.create(
                            物件ID_id=row['物件ID'],
                            支払先コード_id=row['支払先コード'],
                            管理項目コード_id=row['管理項目コード'],
                            レポート日=row['レポート日'],
                            当該月開始月=row['当該月開始月'],
                            当該月終了月=row['当該月終了月'],
                            請求書発行月=row['請求書発行月'],
                            計上日=row['計上日'],
                            請求金額=row['請求金額'],
                            請求消費税=row['請求消費税'],
                            請求税金込=row['請求税金込'],
                            当月支払日=row['当月支払日'],
                            備考=row['備考'],
                            DeleteFlag=row['DeleteFlag'],
                        )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))