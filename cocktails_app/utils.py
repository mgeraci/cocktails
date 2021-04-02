import os
import json

from django.db.models import Count

from cocktails_app.models import Recipe, get_has_session, RECIPE_CATEGORIES


def get_recipes_with_duplicated_names(request):
    has_session = get_has_session(request)
    recipes = Recipe.get(request)

    if (not has_session):
        recipes = recipes.filter(is_public=True)

    try:
        filters = [int(f) for f in request.GET.get('filters').split(',')]
    except:
        filters = [RECIPE_CATEGORIES['COCKTAIL'], RECIPE_CATEGORIES['LARGE_FORMAT']]

    recipes = recipes.filter(category__in=filters)

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
