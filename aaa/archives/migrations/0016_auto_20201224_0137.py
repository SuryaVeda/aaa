# Generated by Django 3.1.3 on 2020-12-24 01:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0015_auto_20201217_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 20, 7, 26, 607171, tzinfo=utc)),
        ),
    ]
