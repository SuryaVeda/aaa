# Generated by Django 3.1.3 on 2020-12-05 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0007_auto_20201205_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 5, 12, 23, 35, 142441, tzinfo=utc)),
        ),
    ]
