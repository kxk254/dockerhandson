# Generated by Django 5.0.7 on 2024-08-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0027_管理項目_管理項目短縮名'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthselect',
            name='MonthSelect',
            field=models.DateField(primary_key=True, serialize=False),
        ),
    ]
