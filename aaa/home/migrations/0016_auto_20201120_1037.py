# Generated by Django 3.1.3 on 2020-11-20 05:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20201120_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 5, 7, 56, 436496, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 5, 7, 56, 438435, tzinfo=utc)),
        ),
    ]
