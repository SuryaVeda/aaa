# Generated by Django 3.1.3 on 2021-02-04 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20210130_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestobj',
            name='date',
            field=models.DateField(default=datetime.date(2021, 2, 4)),
        ),
    ]