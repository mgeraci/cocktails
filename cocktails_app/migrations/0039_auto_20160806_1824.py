# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-06 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0038_auto_20160806_1820'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Step',
            new_name='RecipeIngredient',
        ),
    ]
