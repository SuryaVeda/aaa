# Generated by Django 3.1.3 on 2021-01-30 11:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0073_auto_20210130_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 30, 5, 59, 2, 483569, tzinfo=utc)),
        ),
    ]
