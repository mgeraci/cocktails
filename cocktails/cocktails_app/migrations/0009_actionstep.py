# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0008_step'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionStep',
            fields=[
                ('step_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cocktails_app.Step')),
                ('name', models.CharField(max_length=300)),
            ],
            bases=('cocktails_app.step',),
        ),
    ]