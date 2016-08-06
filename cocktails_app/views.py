# -*- coding: utf-8 -*-

from django.db import models
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from cocktails.localsettings import STATIC_URL

from cocktails_app.forms import SearchForm
from cocktails_app.models import (
    Ingredient, IngredientCategory, Recipe, RecipeIngredient, Source
)


def index(request):
    recipes = Recipe.get(request)
    sources = Source.get_for_recipes(recipes)
    ingredients = Ingredient.get_for_recipes(recipes)

    context = {
        'ingredients': ingredients,
        'recipes': recipes,
        'sources': sources,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/index.html', context)


def source(request, slug):
    source = get_object_or_404(Source, slug=slug)
    recipes = Recipe.get(request, source=source)

    context = {
        'source': source,
        'recipes': recipes,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/source.html', context)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if not recipe.is_public and not request.user.is_authenticated():
        raise Http404

    context = {
        'recipe': recipe,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/recipe.html', context)


def ingredient(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    recipes = ingredient.get_recipes()

    context = {
        'ingredient': ingredient,
        'recipes': recipes,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/ingredient.html', context)


def search(request):
    context = {}

    if not request.GET:
        form = SearchForm()
    else:
        form = SearchForm(request.GET, request=request)
        context['query'] = request.GET.get('query')

        if form.is_valid():
            for k, v in form.process().iteritems():
                context[k] = v
        else:
            context['form_error'] = form.errors['query']

    context['search_form'] = form

    return render(request, 'pages/search.html', context)
