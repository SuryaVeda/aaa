# Generated by Django 3.1.3 on 2021-02-07 23:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0040_auto_20210204_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 7, 17, 54, 39, 140619, tzinfo=utc)),
        ),
    ]
