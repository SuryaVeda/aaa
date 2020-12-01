# Generated by Django 3.1.3 on 2020-11-16 00:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201116_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 0, 35, 44, 318303, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 0, 35, 44, 319191, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/contentfeedImages/%Y/%m/$D/'),
        ),
    ]
