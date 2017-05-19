# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170516_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, height_field='400', null=True, upload_to=profiles.models.upload_location, width_field='400'),
        ),
    ]
