# Generated by Django 3.1.3 on 2020-12-17 18:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0014_auto_20201212_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 12, 52, 12, 676345, tzinfo=utc)),
        ),
    ]
