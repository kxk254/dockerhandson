# Generated by Django 5.0.7 on 2024-08-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0005_rename_請求先_支払先_rename_住所_保証会社_保証会社住所_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='テナント',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
