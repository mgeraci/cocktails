# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 21:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0010_auto_20160709_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionstep',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Action'),
        ),
    ]