# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20170518_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='_userprofile_friends_+', to='profiles.UserProfile'),
        ),
        migrations.DeleteModel(
            name='Friends',
        ),
    ]
