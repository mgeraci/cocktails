# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-24 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0057_auto_20210524_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(default=1, to='cocktails_app.RecipeCategory'),
        ),
    ]
