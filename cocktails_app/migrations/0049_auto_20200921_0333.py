# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-21 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0048_recipe_sort_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['sort_name']},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='type_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Ingredient'),
        ),
    ]