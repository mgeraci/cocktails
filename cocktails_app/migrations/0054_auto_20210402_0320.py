# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-02 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0053_auto_20210402_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipecategory',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
