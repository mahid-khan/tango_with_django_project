# Generated by Django 2.2.28 on 2024-02-09 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_auto_20240208_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=128, unique=True),
        ),
    ]
