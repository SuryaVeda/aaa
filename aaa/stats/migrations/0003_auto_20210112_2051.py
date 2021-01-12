# Generated by Django 3.1.3 on 2021-01-12 20:51

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20210112_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageObj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='requestobj',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 12, 15, 21, 2, 659684, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requestobj',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stats.pageobj'),
        ),
    ]