# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-30 22:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0034_auto_20160730_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientstep',
            name='amount',
        ),
    ]