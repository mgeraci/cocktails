# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-02 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0052_recipecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipecategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]