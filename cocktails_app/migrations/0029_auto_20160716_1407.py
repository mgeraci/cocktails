# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-16 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0028_recipe_glass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='source',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Source'),
        ),
    ]
