# Generated by Django 3.1.3 on 2020-11-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20201121_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetail',
            name='work',
            field=models.ManyToManyField(blank=True, to='accounts.MedicalCollege'),
        ),
    ]
