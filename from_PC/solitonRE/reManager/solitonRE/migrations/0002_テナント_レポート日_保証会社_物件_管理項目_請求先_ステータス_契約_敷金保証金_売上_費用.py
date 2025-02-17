# Generated by Django 5.0.7 on 2024-08-06 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='テナント',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('テナント名', models.CharField(max_length=255)),
                ('テナント住所', models.CharField(max_length=255)),
                ('テナント電話番号', models.CharField(max_length=15)),
                ('テナント担当者名', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='レポート日',
            fields=[
                ('レポート日', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='保証会社',
            fields=[
                ('保証会社コード', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('保証会社名', models.CharField(max_length=100)),
                ('住所', models.CharField(max_length=200)),
                ('担当者名', models.CharField(max_length=100)),
                ('連絡先', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='物件',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('物件名', models.CharField(max_length=100)),
                ('物件住所', models.CharField(max_length=200)),
                ('物件種類', models.CharField(max_length=100)),
                ('建築年月日', models.DateField()),
                ('敷地面積', models.FloatField()),
                ('床面積', models.FloatField()),
                ('構造', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='管理項目',
            fields=[
                ('管理項目コード', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('管理項目印字名', models.CharField(max_length=100)),
                ('管理項目レポート分類区分', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='請求先',
            fields=[
                ('請求先コード', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('請求先名', models.CharField(max_length=100)),
                ('請求先住所', models.CharField(max_length=200)),
                ('請求先担当者', models.CharField(max_length=100)),
                ('請求先電話番号', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ステータス',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('新テナント', models.CharField(max_length=255)),
                ('テナント関連', models.CharField(max_length=255)),
                ('遅延状況', models.CharField(max_length=255)),
                ('検査情報', models.CharField(max_length=255)),
                ('メンテナンス', models.CharField(max_length=255)),
                ('その他', models.CharField(max_length=255)),
                ('特別項目', models.CharField(max_length=255)),
                ('DeleteFlag', models.BooleanField(default=False)),
                ('レポート日', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.レポート日')),
            ],
        ),
        migrations.CreateModel(
            name='契約',
            fields=[
                ('契約番号', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('契約日', models.DateField()),
                ('当初開始日', models.DateField()),
                ('当初終了日', models.DateField()),
                ('現在契約開始日', models.DateField(blank=True)),
                ('現在契約終了日', models.DateField(blank=True)),
                ('賃料金額', models.IntegerField()),
                ('共益費', models.IntegerField()),
                ('契約種類', models.CharField(max_length=100)),
                ('自動更新', models.BooleanField(default=True)),
                ('契約年数', models.CharField(max_length=20)),
                ('更新料有無', models.BooleanField(default=True)),
                ('更新料金額', models.IntegerField()),
                ('解約通知期間', models.CharField(max_length=20)),
                ('居室タイプ', models.CharField(max_length=32)),
                ('平米数', models.FloatField()),
                ('坪数', models.FloatField()),
                ('保証金金額', models.IntegerField()),
                ('保証金月数', models.IntegerField()),
                ('保証有無', models.BooleanField(default=True)),
                ('保証会社名', models.CharField(max_length=100)),
                ('フリーレント', models.IntegerField(blank=True)),
                ('備考', models.CharField(blank=True, max_length=200)),
                ('delete_flag', models.BooleanField(default=False)),
                ('テナントID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.テナント')),
                ('物件ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.物件')),
            ],
        ),
        migrations.CreateModel(
            name='敷金保証金',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('契約区画', models.CharField(max_length=100)),
                ('定借区分', models.CharField(max_length=100)),
                ('種類', models.CharField(max_length=100)),
                ('前月末残高', models.IntegerField()),
                ('当月増額', models.IntegerField(blank=True)),
                ('当月減少', models.IntegerField(blank=True)),
                ('今月末残高', models.IntegerField()),
                ('移動予定日', models.DateField(blank=True)),
                ('DeleteFlag', models.BooleanField(default=False)),
                ('テナントID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.テナント')),
                ('保証会社コード', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.保証会社')),
                ('契約番号', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.契約')),
            ],
        ),
        migrations.CreateModel(
            name='売上',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('該当月開始月', models.DateField()),
                ('該当月終了月', models.DateField()),
                ('請求書発行月', models.DateField()),
                ('入金予定日', models.DateField()),
                ('計上日', models.DateField()),
                ('請求金額', models.IntegerField()),
                ('請求消費税', models.IntegerField()),
                ('請求税金込', models.IntegerField()),
                ('当月入金額', models.IntegerField()),
                ('備考', models.CharField(blank=True, max_length=200)),
                ('DeleteFlag', models.BooleanField(default=False)),
                ('テナントID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.テナント')),
                ('レポート日', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.レポート日')),
                ('契約番号', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.契約')),
                ('物件ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.物件')),
                ('管理項目コード', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.管理項目')),
            ],
        ),
        migrations.CreateModel(
            name='費用',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('当該月開始月', models.DateField()),
                ('当該月終了月', models.DateField()),
                ('請求書発行月', models.DateField()),
                ('計上日', models.DateField()),
                ('請求金額', models.IntegerField()),
                ('請求消費税', models.IntegerField()),
                ('請求税込金', models.IntegerField()),
                ('当月支払日', models.DateField()),
                ('備考', models.CharField(max_length=255)),
                ('DeleteFlag', models.BooleanField(default=False)),
                ('レポート日', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.レポート日')),
                ('物件ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.物件')),
                ('管理項目コード', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.管理項目')),
                ('請求先コード', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solitonRE.請求先')),
            ],
        ),
    ]
