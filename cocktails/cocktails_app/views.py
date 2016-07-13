# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from cocktails.localsettings import STATIC_URL
from util.view import is_safe

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
    steps = []

    for step in recipe.step_set.all():
        steps.append(step.get_actual_instance())

    context = {
        'recipe': recipe,
        'steps': steps,
    }

    return render(request, 'pages/recipe.html', context)


def search(request, slug):
    q = slug.lower()
    ingredient_res = set()
    recipe_res = []

    # TODO don't search with fewer than 3 chars

    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()

    for ingredient in ingredients:
        if ingredient.name.lower().find(q) >= 0:
            ingredient_res.add(ingredient)

    for recipe in recipes:
        print recipe.name
        if recipe.name.lower().find(q) >= 0:
            recipe_res.append(recipe)

        for step in recipe.step_set.all():
            step = step.get_actual_instance()

            if hasattr(step, 'ingredient'):
                print 'ingredient step'

                if step.ingredient.name.lower().find(q) >= 0:
                    ingredient_res.add(step.ingredient)

    if not is_safe(q):
        q = "No special characters allowed"

    context = {
        'query': slug,
    }

    if len(recipe_res) > 0:
        context['recipe_res'] = recipe_res

    if len(ingredient_res) > 0:
        context['ingredient_res'] = ingredient_res

    if len(ingredient_res) == 0 and len(recipe_res) == 0:
        context['no_results'] = True

    return render(request, 'pages/search.html', context)
