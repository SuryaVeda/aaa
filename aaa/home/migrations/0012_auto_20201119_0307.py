# Generated by Django 3.1.3 on 2020-11-18 21:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20201119_0248'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, max_length=400, null=True)),
                ('link_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='link_name',
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 18, 21, 37, 44, 950752, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 18, 21, 37, 44, 952335, tzinfo=utc)),
        ),
        migrations.RemoveField(
            model_name='post',
            name='link',
        ),
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.ManyToManyField(blank=True, null=True, to='home.PostLink'),
        ),
    ]
