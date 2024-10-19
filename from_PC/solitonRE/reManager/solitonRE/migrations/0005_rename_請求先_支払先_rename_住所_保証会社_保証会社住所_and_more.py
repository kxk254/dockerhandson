# Generated by Django 5.0.7 on 2024-08-08 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0004_monthselect'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='請求先',
            new_name='支払先',
        ),
        migrations.RenameField(
            model_name='保証会社',
            old_name='住所',
            new_name='保証会社住所',
        ),
        migrations.RenameField(
            model_name='保証会社',
            old_name='担当者名',
            new_name='保証会社担当者名',
        ),
        migrations.RenameField(
            model_name='保証会社',
            old_name='連絡先',
            new_name='保証会社連絡先',
        ),
        migrations.RenameField(
            model_name='支払先',
            old_name='請求先コード',
            new_name='支払先コード',
        ),
        migrations.RenameField(
            model_name='費用',
            old_name='請求先コード',
            new_name='支払先コード',
        ),
    ]
