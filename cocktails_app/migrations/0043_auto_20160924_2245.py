# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-24 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0042_auto_20160822_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='unit',
            name='after_ingredient',
            field=models.BooleanField(default=False),
        ),
    ]
