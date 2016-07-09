# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from cocktails.localsettings import STATIC_URL

from cocktails_app.models import IngredientCategory
from cocktails_app.models import Ingredient
from cocktails_app.models import Recipe

def index(request):
    categories = IngredientCategory.objects.all()
    recipes = Recipe.objects.all()

    context = {
        'categories': categories,
        'recipes': recipes,
    }

    return render(request, 'pages/index.html', context)

def ingredient_category(request, slug):
    category = get_object_or_404(IngredientCategory, slug=slug)
    ingredients = Ingredient.objects.filter(category=category)

    context = {
        'category': category,
        'ingredients': ingredients,
    }

    return render(request, 'pages/ingredients_category.html', context)

def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    context = {
        'recipe': recipe,
    }

    return render(request, 'pages/recipe.html', context)
