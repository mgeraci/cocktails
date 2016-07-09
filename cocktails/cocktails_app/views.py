# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from cocktails.localsettings import STATIC_URL

from cocktails_app.models import IngredientCategory
from cocktails_app.models import Ingredient

def index(request):
    context = {
        'categories': IngredientCategory.objects.all()
    }

    return render(request, 'pages/index.html', context)

def ingredient_category(request, slug):
    print slug
    category = get_object_or_404(IngredientCategory, slug=slug)
    ingredients = Ingredient.objects.filter(category=category)

    context = {
        'category': category,
        'ingredients': ingredients,
    }

    return render(request, 'pages/ingredients_category.html', context)
