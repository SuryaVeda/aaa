# Generated by Django 3.1.3 on 2021-02-07 23:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20210204_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestobj',
            name='date',
            field=models.DateField(default=datetime.date(2021, 2, 7)),
        ),
    ]
