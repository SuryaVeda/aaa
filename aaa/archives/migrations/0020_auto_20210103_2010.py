# Generated by Django 3.1.3 on 2021-01-03 20:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0019_auto_20201224_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 3, 14, 40, 0, 264315, tzinfo=utc)),
        ),
    ]
