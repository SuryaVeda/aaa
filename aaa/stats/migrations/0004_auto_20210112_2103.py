# Generated by Django 3.1.3 on 2021-01-12 21:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20210112_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestobj',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 12, 15, 33, 26, 611383, tzinfo=utc)),
        ),
    ]