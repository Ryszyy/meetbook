# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20170522_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
