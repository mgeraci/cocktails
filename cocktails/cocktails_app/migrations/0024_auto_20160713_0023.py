# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-13 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0023_auto_20160713_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
