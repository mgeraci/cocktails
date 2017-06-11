from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.forms.models import model_to_dict


class Source(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Source, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('source_url', args=[self.slug])

    def __unicode__(self):
        return self.name

    @classmethod
    def get_for_recipes(cls, recipes):
        return cls.objects.filter(pk__in=recipes.values('source'))


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


class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, default='Alcohol')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IngredientCategory, default='Alcohol')
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Ingredient, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_recipes(self, **kwargs):
        return self.recipe_set.all()

    def get_absolute_url(self):
        return reverse('ingredient_url', args=[self.slug])

    @classmethod
    def get_for_recipes(cls, recipes, **kwargs):
        ingredients = Ingredient.objects.none()

        for recipe in recipes:
            ingredients |= recipe.ingredients.filter(**kwargs)

        return ingredients.distinct()


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    source = models.ForeignKey(Source, blank=True, null=True)
    glass = models.ForeignKey(Glass, blank=True, null=True)
    directions = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('recipe_url', args=[self.slug])

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Recipe, self).save(*args, **kwargs)

    def serialize(self):
        res = model_to_dict(self, exclude=['ingredients'])

        res['glass'] = model_to_dict(Glass.objects.get(id=res['glass']))

        if res['source']:
            res['source'] = model_to_dict(Source.objects.get(id=res['source']))

        recipeingredients = self.recipeingredient_set.all()
        res['ingredients'] = [ri.serialize() for ri in recipeingredients]

        return res

    def __unicode__(self):
        return self.name

    @classmethod
    def get(cls, request, **kwargs):
        if request.user.is_authenticated():
            return cls.objects.filter(**kwargs)
        else:
            return cls.objects.filter(is_public=True, **kwargs)


class Unit(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)
    after_ingredient = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)

    amount_num = models.IntegerField()
    amount_den = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def is_over_one(self):
        return float(self.amount_num) / self.amount_den > 1

    def is_zero(self):
        return not self.amount_num

    def is_rinse(self):
        return self.unit.name == 'rinse'

    def serialize(self):
        res = model_to_dict(self, exclude=['recipe'])
        res['ingredient'] = model_to_dict(Ingredient.objects.get(id=res['ingredient']))

        if res['unit']:
            res['unit'] = model_to_dict(Unit.objects.get(id=res['unit']))

        return res

    def __unicode__(self):
        return self.ingredient.name
