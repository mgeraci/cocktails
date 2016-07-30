# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django import forms
from cocktails.localsettings import STATIC_URL
from util.view import is_safe

from cocktails_app.models import IngredientCategory
from cocktails_app.models import Ingredient
from cocktails_app.models import Recipe
from cocktails_app.models import Source


class search_form(forms.Form):
    query = forms.CharField(required=False, label='',
            widget=forms.TextInput(
                attrs={'placeholder': 'e.g., Rye or Sazerac'}))


def index(request):
    categories = IngredientCategory.objects.all()
    recipes = Recipe.objects.all()
    sources = Source.objects.all()

    context = {
        'categories': categories,
        'recipes': recipes,
        'sources': sources,
        'search_form': search_form(),
    }

    return render(request, 'pages/index.html', context)


def source(request, slug):
    source = get_object_or_404(Source, slug=slug)
    recipes = Recipe.objects.filter(source=source.id)

    context = {
        'source': source,
        'recipes': recipes,
        'search_form': search_form(),
    }

    return render(request, 'pages/source.html', context)


def ingredient_category(request, slug):
    category = get_object_or_404(IngredientCategory, slug=slug)
    ingredients = Ingredient.objects.filter(category=category)

    context = {
        'category': category,
        'ingredients': ingredients,
        'search_form': search_form(),
    }

    return render(request, 'pages/ingredients_category.html', context)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    steps = []
    steps_data = []

    for step in recipe.step_set.all():
        step = step.get_actual_instance()

        if hasattr(step, 'get_step_data'):
            steps_data.append(step.get_step_data())

        steps.append(step)

    context = {
        'recipe': recipe,
        'steps': steps,
        'steps_data': steps_data,
        'search_form': search_form(),
    }

    return render(request, 'pages/recipe.html', context)


def ingredient(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    recipe_res = set()

    if ingredient != None:
        recipes = Recipe.objects.all()

    for recipe in recipes:
        for step in recipe.step_set.all():
            step = step.get_actual_instance()

            if hasattr(step, 'ingredient'):
                if step.ingredient == ingredient:
                    recipe_res.add(recipe)

    context = {
        'ingredient': ingredient,
        'recipes': recipe_res,
        'search_form': search_form(),
    }

    return render(request, 'pages/ingredient.html', context)


def search(request):
    if request.GET.get('query'):
        q_orig = request.GET.get('query')
        q = q_orig.lower()

    ingredient_res = set()
    recipe_ingredients_res = set()
    recipe_titles_res = set()

    # TODO don't search with fewer than 3 chars

    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()

    for ingredient in ingredients:
        if ingredient.name.lower().find(q) >= 0:
            ingredient_res.add(ingredient)

    for recipe in recipes:
        if recipe.name.lower().find(q) >= 0:
            recipe_titles_res.add(recipe)

        for step in recipe.step_set.all():
            step = step.get_actual_instance()

            if hasattr(step, 'ingredient'):
                if step.ingredient.name.lower().find(q) >= 0:
                    ingredient_res.add(step.ingredient)
                    recipe_ingredients_res.add(recipe)

    if not is_safe(q):
        q = "No special characters allowed"

    context = {
        'query': q_orig,
        'search_form': search_form(),
    }

    if len(recipe_titles_res) > 0:
        context['recipe_titles_res'] = recipe_titles_res

    if len(recipe_ingredients_res) > 0:
        context['recipe_ingredients_res'] = recipe_ingredients_res

    if len(ingredient_res) > 0:
        context['ingredient_res'] = ingredient_res

    if len(ingredient_res) == 0 and len(recipe_ingredients_res) == 0 and len(recipe_titles_res) == 0:
        context['no_results'] = True

    return render(request, 'pages/search.html', context)
