# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-24 01:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0055_recipe_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(blank=True, default=1, to='cocktails_app.RecipeCategory'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='legacy_recipe_set', to='cocktails_app.RecipeCategory'),
        ),
    ]
