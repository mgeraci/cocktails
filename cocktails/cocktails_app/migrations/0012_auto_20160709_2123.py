# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 21:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0011_auto_20160709_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionstep',
            name='action',
        ),
        migrations.RemoveField(
            model_name='actionstep',
            name='step_ptr',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.DeleteModel(
            name='ActionStep',
        ),
    ]