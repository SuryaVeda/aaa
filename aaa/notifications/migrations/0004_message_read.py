# Generated by Django 3.1.3 on 2021-01-30 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20210130_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
