# Generated by Django 3.1.3 on 2020-12-06 07:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_auto_20201205_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 6, 2, 13, 20, 656260, tzinfo=utc)),
        ),
    ]