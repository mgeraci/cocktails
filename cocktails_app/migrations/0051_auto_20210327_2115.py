# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-27 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0050_auto_20200921_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
