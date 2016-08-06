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
    source = models.ForeignKey(Source, blank=True, null=True)
    glass = models.ForeignKey(Glass, blank=True, null=True)
    directions = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Recipe, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, default="Alcohol")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

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


class Unit(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Step(models.Model, RealInstanceProvider):
    recipe = models.ForeignKey(Recipe)
    ingredient_foo = models.ForeignKey(Ingredient)

    amount_num_foo = models.IntegerField()
    amount_den_foo = models.IntegerField(default=1)
    unit_foo = models.ForeignKey(Unit, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def is_over_one(self):
        return float(self.amount_num) / self.amount_den > 1

    def is_zero(self):
        return not not self.amount_num

    def is_rinse(self):
        return self.unit.name == 'rinse'

    def __unicode__(self):
        return self.ingredient.name


'''
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)

    amount_num = models.IntegerField()
    amount_den = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def is_over_one(self):
        return float(self.amount_num) / self.amount_den > 1

    def is_zero(self):
        return not not self.amount_num

    def is_rinse(self):
        return self.unit.name == 'rinse'

    def __unicode__(self):
        return self.ingredient.name
'''


class IngredientStep(Step):
    ingredient = models.ForeignKey(Ingredient)
    amount_num = models.IntegerField()
    amount_den = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, null=True, blank=True)

    def recipe_print(self):
        if self.unit:
            if self.amount > 1.0:
                unit = self.unit.plural
            else:
                unit = self.unit.name

            return u'{}/{} {} {}'.format(
                self.amount_num, self.amount_den, unit,
                self.ingredient.name
            )
        else:
            return u'{}/{} {}'.format(
                self.amount_num, self.amount_den, self.ingredient.name
            )

    def get_step_data(self):
        unit = None

        if self.unit:
            unit = self.unit

        return {
            'amount_num': self.amount_num,
            'amount_den': self.amount_den,
            'ingredient': self.ingredient.name,
            'unit': unit,
        }

    def __unicode__(self):
        return self.ingredient.name
