# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-10 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0019_auto_20160710_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientstep',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
