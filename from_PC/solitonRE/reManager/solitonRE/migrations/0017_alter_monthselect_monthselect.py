# Generated by Django 5.0.7 on 2024-08-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0016_rename_請求税込金_費用_請求税金込'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthselect',
            name='MonthSelect',
            field=models.IntegerField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
