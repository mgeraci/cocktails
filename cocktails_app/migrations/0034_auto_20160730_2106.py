# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-30 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0033_auto_20160730_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientstep',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Unit'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='glass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Glass'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Source'),
        ),
    ]
