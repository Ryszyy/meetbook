# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 07:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170603_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.GroupProfile')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='time',
            field=models.ManyToManyField(blank=True, to='profiles.FreeTime'),
        ),
    ]
