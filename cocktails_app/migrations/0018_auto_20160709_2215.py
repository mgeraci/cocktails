# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0017_auto_20160709_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientstep',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ingredientstep',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Unit'),
        ),
    ]