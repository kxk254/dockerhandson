# Generated by Django 5.0.7 on 2024-08-12 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solitonRE', '0026_テナント_テナント短縮名'),
    ]

    operations = [
        migrations.AddField(
            model_name='管理項目',
            name='管理項目短縮名',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
