# Generated by Django 3.1.3 on 2021-01-23 01:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0034_auto_20210112_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 22, 20, 28, 16, 961079, tzinfo=utc)),
        ),
    ]
