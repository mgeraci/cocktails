from __future__ import unicode_literals
from django.db import models

class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, default="Alcohol")
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IngredientCategory, default="Alcohol")

    def __unicode__(self):
        return u'{} - {}'.format(self.category, self.name)
