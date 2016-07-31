# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from cocktails.localsettings import STATIC_URL

from cocktails_app.forms import SearchForm
from cocktails_app.models import (
    Ingredient, IngredientCategory, Recipe, Source
)


def index(request):
    categories = IngredientCategory.objects.all()
    recipes = Recipe.objects.all()
    sources = Source.objects.all()

    context = {
        'categories': categories,
        'recipes': recipes,
        'sources': sources,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/index.html', context)


def source(request, slug):
    source = get_object_or_404(Source, slug=slug)
    recipes = Recipe.objects.filter(source=source.id)

    context = {
        'source': source,
        'recipes': recipes,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/source.html', context)


def ingredient_category(request, slug):
    category = get_object_or_404(IngredientCategory, slug=slug)
    ingredients = Ingredient.objects.filter(category=category)

    context = {
        'category': category,
        'ingredients': ingredients,
        'search_form': SearchForm(),
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
        'search_form': SearchForm(),
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
        'search_form': SearchForm(),
    }

    return render(request, 'pages/ingredient.html', context)


def search(request):
    context = {}

    if not request.GET:
        form = SearchForm()
    else:
        form = SearchForm(request.GET)
        context['query'] = request.GET.get('query')

        if form.is_valid():
            for k, v in form.process().iteritems():
                context[k] = v
        else:
            context['invalid_search'] = True

    context['search_form'] = form

    return render(request, 'pages/search.html', context)
