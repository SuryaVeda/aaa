# Generated by Django 3.1.3 on 2021-01-03 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
