# Generated by Django 3.1.3 on 2021-01-03 21:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_auto_20210103_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 3, 16, 24, 19, 604353, tzinfo=utc)),
        ),
    ]
