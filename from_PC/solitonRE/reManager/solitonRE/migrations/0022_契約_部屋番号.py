# Generated by Django 5.0.7 on 2024-08-11 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0021_delete_defaultinput'),
    ]

    operations = [
        migrations.AddField(
            model_name='契約',
            name='部屋番号',
            field=models.CharField(default=1, max_length=24),
            preserve_default=False,
        ),
    ]
