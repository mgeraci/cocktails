# -*- coding: utf-8 -*-

import re
import json

from django.db import models
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

from cocktails.localsettings import STATIC_URL

from cocktails_app.forms import SearchForm
from cocktails_app.models import (
    Glass, Ingredient, IngredientCategory, Recipe, RecipeIngredient, Source
)


# helpers
# -----------------------------------------------------------------------------

MOBILE_RE = re.compile(
    r".*(iphone|mobile|androidtouch)",
    re.IGNORECASE
)


def get_is_api(request):
    return request.GET.get('api')


# views
# -----------------------------------------------------------------------------

@csrf_exempt
def api_login(request):
    try:
        params = json.loads(request.POST.items()[0][0])
    except:
        params = request.POST

    username = params.get('username')
    password = params.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({ 'session_key': request.session.session_key })
    else:
        return JsonResponse({ 'error': True })


def index(request):
    # redirect to the recipes listing page if on mobile
    if MOBILE_RE.match(request.META['HTTP_USER_AGENT']):
        return redirect('recipes_url')

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
        'title': u'Recipes from {}'.format(source.name),
        'list_items': recipes,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/list.html', context)


def sources(request):
    recipes = Recipe.get(request)
    sources = Source.get_for_recipes(recipes)

    context = {
        'title': 'Sources',
        'list_items': sources,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/list.html', context)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if not recipe.is_public and not request.user.is_authenticated():
        raise Http404

    context = {
        'recipe': recipe,
    }

    if get_is_api(request):
        return JsonResponse(recipe.serialize())
    else:
        context['search_form'] = SearchForm()
        return render(request, 'pages/recipe.html', context)


def recipes(request):
    recipes = Recipe.get(request)

    context = {
        'title': 'Recipes',
        'list_items': recipes,
    }

    if get_is_api(request):
        pairs = [{
            'name': recipe.name,
            'slug': recipe.slug
        } for recipe in recipes]

        return JsonResponse({ 'recipes': pairs })
    else:
        context['search_form'] = SearchForm()
        return render(request, 'pages/list.html', context)


def ingredient(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    recipes = ingredient.get_recipes()

    context = {
        'title': u'Recipes with {}'.format(ingredient.name),
        'list_items': recipes,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/list.html', context)


def ingredients(request):
    recipes = Recipe.get(request)
    ingredients = Ingredient.get_for_recipes(recipes)

    context = {
        'title': 'Ingredients',
        'list_items': ingredients,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/list.html', context)


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
