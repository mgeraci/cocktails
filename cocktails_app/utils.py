import os
import json

from django.db.models import Count

from cocktails_app.models import Recipe, Glass, RecipeTag, get_has_session, RECIPE_CATEGORIES


def filter_recipes(recipes, request):
    default_categories = [
        RECIPE_CATEGORIES['COCKTAIL'],
        RECIPE_CATEGORIES['LARGE_FORMAT'],
    ]

    try:
        categories = default_categories

        if request.path == '/search/':
            categories = [
                RECIPE_CATEGORIES['COCKTAIL'],
                RECIPE_CATEGORIES['LARGE_FORMAT'],
                RECIPE_CATEGORIES['INGREDIENT'],
            ]
        else:
            categories = [int(c) for c in request.GET.get('categories').split(',')]
    except:
        categories = default_categories

    try:
        glasses = [int(g) for g in request.GET.get('glasses').split(',')]
    except:
        glasses = None

    try:
        tags = [int(t) for t in request.GET.get('tags').split(',')]
    except:
        tags = None

    recipes = recipes.filter(category__in=categories)

    if glasses:
        recipes = recipes.filter(glass__in=glasses)

    if tags:
        recipes = recipes.filter(tags__in=tags)

    return recipes


def decorate_recipe_list_with_sources(recipes):
    recipes_with_duplicated_names = set(
        Recipe.objects.values('name').annotate(Count('id')).filter(id__count__gt=1).values_list('name', flat=True)
    )

    for recipe in recipes:
        if recipe.name in recipes_with_duplicated_names and recipe.source:
            recipe.name = u'{} ({})'.format(recipe.name, recipe.source)

    return recipes


def get_recipes_with_duplicated_names(request):
    has_session = get_has_session(request)
    recipes = Recipe.get(request)

    if (not has_session):
        recipes = recipes.filter(is_public=True)

    recipes = filter_recipes(recipes, request)

    return decorate_recipe_list_with_sources(recipes)


def get_static_path(file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest_path = dir_path + "/static/dist/manifest.json"

    with open(manifest_path) as data:
        data = json.load(data)
        return data.get(file)
