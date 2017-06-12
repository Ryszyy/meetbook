# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170605_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupprofile',
            name='date',
        ),
        migrations.AddField(
            model_name='freetime',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='profiles.UserProfile'),
        ),
    ]