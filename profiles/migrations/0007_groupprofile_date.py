# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_freetime_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
