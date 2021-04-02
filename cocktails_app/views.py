# -*- coding: utf-8 -*-

import re
import json

from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

from cocktails.localsettings import STATIC_URL, VIEWER_USERNAME

from cocktails_app.forms import SearchForm
from cocktails_app.models import (
    Glass, Ingredient, IngredientCategory, Recipe, RecipeIngredient, Source,
)
from cocktails_app.utils import get_recipes_with_duplicated_names
from cocktails_app.sharing import decrypt, encrypt


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
        params = request.body.decode('utf-8')
        params = json.loads(params)
    except:
        params = request.POST

    username = VIEWER_USERNAME
    password = params.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({ 'session_key': request.session.session_key })
    else:
        return JsonResponse({ 'error': True })

def site_login(request):
    user = None
    username = VIEWER_USERNAME
    password = request.POST.get('password', None)
    post_login_url = request.POST.get('next')

    # default to the index page if missing, or if it's not a relative path,
    # and check that it's not a protocol-less url (//www.example.com)
    if not post_login_url or post_login_url[0] != '/' or post_login_url[1] == '/':
        post_login_url = 'index_url'

    if password:
        user = authenticate(username=username, password=password)

    context = {
        'buttons': [
            { 'number': 1, 'letters': '' },
            { 'number': 2, 'letters': 'ABC' },
            { 'number': 3, 'letters': 'DEF' },
            { 'number': 4, 'letters': 'GHI' },
            { 'number': 5, 'letters': 'JKL' },
            { 'number': 6, 'letters': 'MNO' },
            { 'number': 7, 'letters': 'PQRS' },
            { 'number': 8, 'letters': 'TUV' },
            { 'number': 9, 'letters': 'WXYZ' },
            { 'number': None, 'letters': None },
            { 'number': 0, 'letters': '+' },
            { 'number': None, 'letters': None },
        ]
    }

    if user is not None:
        login(request, user)
        return redirect(post_login_url)
    elif password:
        context['error'] = True

    return render(request, 'pages/login.html', context)

def index(request):
    # redirect to the recipes listing page if on mobile
    if MOBILE_RE.match(request.META['HTTP_USER_AGENT']):
        return redirect('recipes_url')

    recipes = get_recipes_with_duplicated_names(request)
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

    if len(recipes) == 0 and not request.user.is_authenticated():
        return redirect('/login/?next=/source/{}'.format(slug))

    if get_is_api(request):
        pairs = [{
            'name': recipe.name,
            'slug': recipe.slug
        } for recipe in recipes]

        return JsonResponse({ 'recipes': pairs });
    else:
        context = {
            'title': u'Recipes from {}'.format(source.name),
            'list_items': recipes,
            'search_form': SearchForm(),
            'source': source,
        }

        return render(request, 'pages/list.html', context)


def sources(request):
    recipes = Recipe.get(request)
    sources = Source.get_for_recipes(recipes)

    if get_is_api(request):
        pairs = [{
            'name': source.name,
            'slug': source.slug
        } for source in sources]

        return JsonResponse({ 'sources': pairs });
    else:
        context = {
            'title': 'Sources',
            'list_items': sources,
            'search_form': SearchForm(),
        }

        return render(request, 'pages/list.html', context)


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if not recipe.is_public and not request.user.is_authenticated():
        return redirect('/login/?next=/recipe/{}'.format(slug))

    if get_is_api(request):
        return JsonResponse(recipe.serialize())
    else:
        context = {
            'recipe': recipe,
            'share_link': '/recipe/l/{}'.format(encrypt(recipe.slug)),
            'search_form': SearchForm(),
        }

        return render(request, 'pages/recipe.html', context)


def recipe_share(request, slug):
    decrypted_slug = decrypt(slug)
    recipe = get_object_or_404(Recipe, slug=decrypted_slug)

    context = {
        'recipe': recipe,
        'search_form': SearchForm(),
    }

    return render(request, 'pages/recipe.html', context)


def recipes(request):
    recipes = get_recipes_with_duplicated_names(request);

    context = {
        'title': 'Recipes',
        'list_items': recipes,
    }

    if get_is_api(request):
        res = [{
            'name': recipe.name,
            'slug': recipe.slug
        } for recipe in recipes]

        return JsonResponse({ 'recipes': res })
    else:
        context['search_form'] = SearchForm()
        return render(request, 'pages/list.html', context)


def ingredient(request, slug):
    ingredient = get_object_or_404(Ingredient, slug=slug)
    recipes = ingredient.get_recipes(request).distinct()

    if get_is_api(request):
        pairs = [{
            'name': recipe.name,
            'slug': recipe.slug
        } for recipe in recipes]

        return JsonResponse({ 'recipes': pairs });
    else:
        context = {
            'title': u'Recipes with {}'.format(ingredient.name),
            'list_items': recipes,
            'search_form': SearchForm(),
            'ingredient': ingredient,
        }

        return render(request, 'pages/list.html', context)


def ingredients(request):
    recipes = Recipe.get(request)
    ingredients = Ingredient.get_for_recipes(recipes)

    if get_is_api(request):
        pairs = [{
            'name': ingredient.name,
            'slug': ingredient.slug
        } for ingredient in ingredients]

        return JsonResponse({ 'ingredients': pairs });
    else:
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
            for k, v in form.process().items():
                context[k] = v
        else:
            context['form_error'] = form.errors['query']

    if get_is_api(request):
        res = {}

        for k, v in context.items():
            if isinstance(v, QuerySet) or isinstance(v, list):
                res[k] = [{'name': i.name, 'slug': i.slug} for i in v]
            else:
                res[k] = v

        return JsonResponse(res);
    else:
        context['search_form'] = form

        return render(request, 'pages/search.html', context)


def apple_app_site_association(request):
    return JsonResponse({
        'applinks': {
            'apps': [],
            'details': [{
                'appID': 'FG7AYYTX96.com.geraci.martinez.cocktails.app',
                'paths': ['*']
            }]
        }
    })
