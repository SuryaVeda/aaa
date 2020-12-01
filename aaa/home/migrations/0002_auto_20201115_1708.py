# Generated by Django 3.1.3 on 2020-11-15 11:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='commentsImages/%Y/%m/$D/'),
        ),
        migrations.AddField(
            model_name='comment',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='link_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='commentsPosts/pdf/%Y/%m/$D/'),
        ),
        migrations.AddField(
            model_name='comment',
            name='pdf_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='link_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='homePosts/pdf/%Y/%m/$D/'),
        ),
        migrations.AddField(
            model_name='post',
            name='pdf_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 15, 11, 38, 31, 319694, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 15, 11, 38, 31, 321103, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='contentfeedImages/%Y/%m/$D/'),
        ),
    ]
