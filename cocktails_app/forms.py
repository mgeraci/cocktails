from django import forms
from util.view import is_safe

from cocktails.localsettings import STATIC_URL
from cocktails_app.models import Ingredient, Recipe


def validate_no_special_chars(text):
    if not is_safe(text):
        raise forms.ValidationError('No special characters allowed')

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False, label='', validators=[validate_no_special_chars],
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g., Rye or Sazerac'}))

    def process(self):
        cleaned_data = self.cleaned_data
        q = cleaned_data['query'].lower()

        ingredient_res = set()
        recipe_ingredients_res = set()
        recipe_titles_res = set()

        ingredients = Ingredient.objects.all()
        recipes = Recipe.objects.all()

        # ingredients
        for ingredient in ingredients:
            if ingredient.name.lower().find(q) >= 0:
                ingredient_res.add(ingredient)

        for recipe in recipes:
            # recipe names
            if recipe.name.lower().find(q) >= 0:
                recipe_titles_res.add(recipe)

            # ingredients in recipes
            for step in recipe.step_set.all():
                step = step.get_actual_instance()

                if hasattr(step, 'ingredient'):
                    if step.ingredient.name.lower().find(q) >= 0:
                        ingredient_res.add(step.ingredient)
                        recipe_ingredients_res.add(recipe)

        return {
            'recipe_titles_res': recipe_titles_res,
            'recipe_ingredients_res': recipe_ingredients_res,
            'ingredient_res': ingredient_res,
            'no_results': (
                len(ingredient_res) == 0 and
                len(recipe_ingredients_res) == 0 and
                len(recipe_titles_res) == 0
            )
        }
