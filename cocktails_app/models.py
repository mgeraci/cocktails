from __future__ import unicode_literals
import re
import uuid
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.forms.models import model_to_dict

from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session

from cocktails.localsettings import PRODUCTION_ROOT, DEBUG
from cocktails_app.unique_slugify import unique_slugify

RECIPE_CATEGORIES = {
    'COCKTAIL': 1,
    'LARGE_FORMAT': 2,
    'INGREDIENT': 3,
}

GLASSES = {
    'COUPE': 1,
    'ROCKS': 2,
    'COLLINS': 3,
    'FLUTE': 4,
    'SNIFTER': 5,
    'MUG': 6,
    'TIKI': 7,
    'PILSNER': 8,
    'NICK_NORA': 9,
    'PINEAPPLE': 10,
    'COCONUT': 11,
    'JULEP': 12,
    'MARTINI': 13,
}

# authentication helper
# checks for either a logged in user, or a valid session id passed in the
# request header
def get_has_session(request):
    # first, check the request user
    if request.user.is_authenticated:
        return True

    # next, check the request for a valid sessionid
    sessionid = None

    try:
        sessionid = request.META.get('HTTP_SESSIONID')
    except:
        pass

    try:
        session = Session.objects.get(session_key=sessionid)
        session.get_decoded()[SESSION_KEY]
        return True
    except (Session.DoesNotExist, KeyError):
        return False

    # default to false
    return False


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

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        return self.name

    @classmethod
    def get_for_recipes(cls, recipes):
        return cls.objects.filter(pk__in=recipes.values('source'))


class Glass(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    should_show_glass_label = models.BooleanField(default=True) # TODO remove

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Glasses'

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Glass, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, default='Alcohol')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Ingredient categories'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IngredientCategory, default='Alcohol', on_delete=models.CASCADE)
    type_of = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['name']

    # add a slug on save, if one doesn't exist
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Ingredient, self).save(*args, **kwargs)

    def __str__(self):
        return u'{}'.format(self.name)

    def get_recipes(self, request, **kwargs):
        inherited_ingredients = self.ingredient_set.all()
        inherited_recipes = Recipe.objects.filter(ingredients__in=inherited_ingredients)
        all_recipes = self.recipe_set.all() | inherited_recipes

        if get_has_session(request):
            return all_recipes
        else:
            return all_recipes.filter(is_public=True, **kwargs)

    def get_absolute_url(self):
        return reverse('ingredient_url', args=[self.slug])

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    @classmethod
    def get_for_recipes(cls, recipes, **kwargs):
        ingredients = Ingredient.objects.none()
        ingredients_type_of = Ingredient.objects.none()
        query = kwargs.get('q') or ''

        for recipe in recipes:
            ingredients |= recipe.ingredients.filter(name__icontains=query)
            ingredients_type_of |= recipe.ingredients.filter(type_of__name__icontains=query)

        return (ingredients | ingredients_type_of).distinct()


class RecipeCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Recipe categories'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    sort_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    encrypted_slug = models.CharField(max_length=200, default=uuid.uuid4)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.CASCADE)
    glass = models.ForeignKey(Glass, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(RecipeCategory, default=RECIPE_CATEGORIES['COCKTAIL'], related_name='legacy_recipe_set', on_delete=models.CASCADE)
    tags = models.ManyToManyField(RecipeTag)
    directions = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    class Meta:
        ordering = ['sort_name']

    def get_absolute_url(self):
        return reverse('recipe_url', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)

        self.sort_name = re.sub(r"^(the|el|la|los|las|le|les) ", "", self.name.lower())

        super(Recipe, self).save(*args, **kwargs)

    def serialize(self):
        res = model_to_dict(self, exclude=['ingredients'])

        if res['glass']:
            res['glass'] = model_to_dict(Glass.objects.get(id=res['glass']))

        if res['source']:
            res['source'] = model_to_dict(Source.objects.get(id=res['source']))

        if res['tags']:
            res['tags'] = [model_to_dict(RecipeTag.objects.get(id=tag.id)) for tag in res['tags']]

        recipeingredients = self.recipeingredient_set.all()
        res['ingredients'] = [ri.serialize() for ri in recipeingredients]

        res['share_link'] = '/recipe/{}'.format(res['slug'])

        if not res['is_public']:
            res['share_link'] = '/recipe/l/{}'.format(self.encrypted_slug)

        if DEBUG == False:
            res['share_link'] = '{}{}'.format(PRODUCTION_ROOT, res['share_link'])

        return res

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, request, **kwargs):
        if get_has_session(request):
            return cls.objects.filter(**kwargs)
        else:
            return cls.objects.filter(is_public=True, **kwargs)


class Unit(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)
    after_ingredient = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    amount_num = models.IntegerField()
    amount_den = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.ingredient.name
