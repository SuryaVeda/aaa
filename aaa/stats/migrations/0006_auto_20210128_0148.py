# Generated by Django 3.1.3 on 2021-01-28 01:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20210123_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestobj',
            name='date',
            field=models.DateField(default=datetime.date(2021, 1, 28)),
        ),
    ]
