# Generated by Django 3.1.3 on 2021-01-07 20:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0063_auto_20210107_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 7, 14, 30, 32, 856057, tzinfo=utc)),
        ),
    ]
