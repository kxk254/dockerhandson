# Generated by Django 5.0.7 on 2024-08-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0017_alter_monthselect_monthselect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthselect',
            name='MonthSelect',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
