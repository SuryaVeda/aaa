# Generated by Django 3.1.3 on 2021-01-30 16:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0038_auto_20210130_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 30, 11, 11, 3, 798409, tzinfo=utc)),
        ),
    ]
