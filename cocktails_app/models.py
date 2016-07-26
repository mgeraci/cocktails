from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from util.model import RealInstanceProvider


class Source(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Source, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Glass(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Glass, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    source = models.ForeignKey(Source, blank=True, default='', null=True)
    glass = models.ForeignKey(Glass, blank=True, default='', null=True)
    directions = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Recipe, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Step(models.Model, RealInstanceProvider):
    order = models.PositiveSmallIntegerField(default=0)
    recipe = models.ForeignKey(Recipe)

    class Meta:
        ordering = ['recipe', 'order']

    def __unicode__(self):
        return u'{} - {}'.format(self.recipe, self.order)


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
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Ingredient, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{} - {}'.format(self.category, self.name)


class IngredientStep(Step):
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(default=1)
    unit = models.ForeignKey(Unit, default=1, null=True, blank=True)

    def recipe_print(self):
        if self.unit:
            if self.amount > 1.0:
                unit = self.unit.plural
            else:
                unit = self.unit.name

            return u'{} {} {}'.format(self.amount, unit, self.ingredient.name)
        else:
            return u'{} {}'.format(self.amount, self.ingredient.name)

    def get_step_data(self):
        unit = None

        if self.unit:
            unit = self.unit

        return {
            'amount': self.amount,
            'ingredient': self.ingredient.name,
            'unit': unit,
        }

    def __unicode__(self):
        return self.ingredient.name
