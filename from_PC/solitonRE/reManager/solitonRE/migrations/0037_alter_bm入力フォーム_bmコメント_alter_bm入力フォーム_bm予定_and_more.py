# Generated by Django 5.0.7 on 2024-08-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0036_bm入力フォーム_bm予定数_bm入力フォーム_bm回数'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bm入力フォーム',
            name='BMコメント',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bm入力フォーム',
            name='BM予定',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='bm入力フォーム',
            name='BM実施',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
