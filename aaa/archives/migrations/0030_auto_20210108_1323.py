# Generated by Django 3.1.3 on 2021-01-08 13:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0029_auto_20210108_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 8, 7, 53, 59, 33575, tzinfo=utc)),
        ),
    ]
