# Generated by Django 3.1.3 on 2021-01-12 19:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0031_auto_20210110_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 12, 14, 22, 0, 303889, tzinfo=utc)),
        ),
    ]