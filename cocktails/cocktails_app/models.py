from __future__ import unicode_literals
from django.db import models
from util.model import RealInstanceProvider


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Step(models.Model, RealInstanceProvider):
    order = models.PositiveSmallIntegerField(default=0)
    recipe = models.ForeignKey(Recipe)

    class Meta:
        ordering = ['recipe', 'order']

    def __unicode__(self):
        return u'{} - {}'.format(self.recipe, self.order)


class Action(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name


class ActionStep(Step):
    action = models.ForeignKey(Action)

    def recipe_print(self):
        return self.action.name

    def __unicode__(self):
        return self.action.name


class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, default="Alcohol")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IngredientCategory, default="Alcohol")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'{} - {}'.format(self.category, self.name)


class IngredientStep(Step):
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit, null=True, blank=True)

    def recipe_print(self):
        if self.amount > 1.0:
            unit = self.unit.plural
        else:
            unit = self.unit.name

        return u'{} {} {}'.format(self.amount, unit, self.ingredient.name)

    def __unicode__(self):
        return self.ingredient.name
