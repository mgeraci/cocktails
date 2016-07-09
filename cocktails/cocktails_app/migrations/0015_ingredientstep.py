# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-09 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails_app', '0014_actionstep'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientStep',
            fields=[
                ('step_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cocktails_app.Step')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocktails_app.Ingredient')),
            ],
            bases=('cocktails_app.step',),
        ),
    ]