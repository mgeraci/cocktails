# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cocktails_app', '0002_delete_ingredientcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Alcohol', max_length=200)),
            ],
        ),
    ]
