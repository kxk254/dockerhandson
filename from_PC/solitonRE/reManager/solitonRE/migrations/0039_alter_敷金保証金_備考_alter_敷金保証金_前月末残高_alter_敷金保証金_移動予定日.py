# Generated by Django 5.0.7 on 2024-09-21 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0038_remove_bmitems_bm予定数_remove_bmitems_bm回数_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='敷金保証金',
            name='備考',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='敷金保証金',
            name='前月末残高',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='敷金保証金',
            name='移動予定日',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
