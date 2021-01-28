# Generated by Django 3.1.3 on 2021-01-28 01:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0071_auto_20210123_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='conference',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 27, 20, 18, 53, 87974, tzinfo=utc)),
        ),
    ]