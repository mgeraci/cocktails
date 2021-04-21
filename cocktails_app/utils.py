import os
import json

from django.db.models import Count

from cocktails_app.models import Recipe, get_has_session, RECIPE_CATEGORIES


def get_recipes_with_duplicated_names(request):
    has_session = get_has_session(request)
    recipes = Recipe.get(request)

    if (not has_session):
        recipes = recipes.filter(is_public=True)

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

    if glasses:
        recipes = recipes.filter(category__in=categories, glass__in=glasses)
    else:
        recipes = recipes.filter(category__in=categories)

    recipes_with_duplicated_names = set(
        Recipe.objects.values('name').annotate(Count('id')).filter(id__count__gt=1).values_list('name', flat=True)
    )

    for recipe in recipes:
        if recipe.name in recipes_with_duplicated_names and recipe.source:
            recipe.name = u'{} ({})'.format(recipe.name, recipe.source)

    return recipes


def get_static_path(file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    manifest_path = dir_path + "/static/dist/manifest.json"

    with open(manifest_path) as data:
        data = json.load(data)
        return data.get(file)
