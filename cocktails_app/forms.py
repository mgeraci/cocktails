from django import forms

from cocktails.localsettings import STATIC_URL
from cocktails_app.models import Ingredient, Recipe


OK_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?:"

def is_safe(str):
    return [x for x in str if x.lower() not in OK_CHARS] == []


def validate_no_special_chars(text):
    if not is_safe(text):
        raise forms.ValidationError('No special characters allowed')


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        validators=[validate_no_special_chars],
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g., Rye or Sazerac'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(SearchForm, self).__init__(*args, **kwargs)

    def process(self):
        cleaned_data = self.cleaned_data
        q = cleaned_data['query'].lower()

        recipes = Recipe.get(self.request)

        title_recipes = recipes.filter(name__icontains=q).distinct()
        ingredients = Ingredient.get_for_recipes(recipes, name__icontains=q).distinct()
        ingredient_recipes = Recipe.objects.filter(ingredients__in=ingredients).distinct()

        return {
            'recipe_titles_res': title_recipes,
            'recipe_ingredients_res': ingredient_recipes,
            'ingredient_res': ingredients,
            'no_results': (
                len(ingredients) == 0 and
                len(ingredient_recipes) == 0 and
                len(title_recipes) == 0
            )
        }
