# Generated by Django 3.1.3 on 2021-02-04 14:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0039_auto_20210130_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 4, 8, 38, 27, 18270, tzinfo=utc)),
        ),
    ]
