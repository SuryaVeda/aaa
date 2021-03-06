# Generated by Django 3.1.3 on 2020-11-18 21:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20201118_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAdd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='contentfeedImages/%Y/%m/$D/')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 18, 21, 14, 53, 476900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 18, 21, 14, 53, 477970, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='post',
            name='img1',
            field=models.ManyToManyField(blank=True, null=True, to='home.ImageAdd'),
        ),
    ]
