# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-21 04:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0049_auto_20200921_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='type_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Ingredient'),
        ),
    ]