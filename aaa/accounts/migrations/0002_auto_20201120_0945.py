# Generated by Django 3.1.3 on 2020-11-20 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='about',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='achievements',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='experiance',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='qualification',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='quotes',
        ),
        migrations.CreateModel(
            name='ProfileDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=50, null=True)),
                ('details', models.CharField(blank=True, max_length=1500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='details',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.ProfileDetail'),
        ),
    ]
