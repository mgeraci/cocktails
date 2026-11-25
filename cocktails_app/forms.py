from django import forms

from cocktails.localsettings import STATIC_URL
from cocktails_app.models import Ingredient, Recipe, get_has_session
from cocktails_app.utils import (
    get_recipes_with_duplicated_names,
    decorate_recipe_list_with_sources,
    SEARCH_TOKEN_SEPARATOR,
)


OK_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?:"

# max number of tokens used for tokenized search
MAX_SEARCH_TOKENS = 5

def is_safe(str):
    return [x for x in str if x.lower() not in OK_CHARS] == []


def validate_no_special_chars(text):
    if not is_safe(text.replace(SEARCH_TOKEN_SEPARATOR, '')):
        raise forms.ValidationError('No special characters allowed')


def split_query_tokens(query):
    tokens = [
        token.strip().lower()
        for token in query.split(SEARCH_TOKEN_SEPARATOR)
    ]
    unique_tokens = list(dict.fromkeys(tokens))

    return unique_tokens[:MAX_SEARCH_TOKENS]


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
        has_session = get_has_session(self.request)

        recipes = list(get_recipes_with_duplicated_names(self.request))
        tokens = split_query_tokens(q)

        if len(tokens) > 1:
            return self.process_tokenized(tokens, has_session, recipes)

        title_recipes = list(filter(lambda recipe: q in recipe.name.lower(), recipes))
        ingredients = list(Ingredient.get_for_recipes(recipes, q=q))
        ingredient_recipes = decorate_recipe_list_with_sources(
            Recipe.objects.filter(ingredients__in=ingredients).distinct()
        )

        if not has_session:
            ingredient_recipes = ingredient_recipes.filter(is_public=True)

        ingredient_recipes = list(ingredient_recipes)

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

    def process_tokenized(self, tokens, has_session, recipes):
        ''' Handle searches for multiple items; return only recipes. '''
        recipe_id_sets = []

        for token in tokens:
            recipe_ids = set()
            token_ingredients = list(Ingredient.get_for_recipes(recipes, q=token))
            recipe_ids |= {
                recipe.id for recipe in
                decorate_recipe_list_with_sources(
                    Recipe.objects.filter(
                        ingredients__in=token_ingredients
                    ).distinct()
                )
                if has_session or recipe.is_public
            }

            recipe_id_sets.append(recipe_ids)

        matched_ids = set.intersection(*recipe_id_sets)

        # rebuild the results from fresh instances; the recipes list above was
        # already decorated in place, so it can't be re-decorated
        ingredient_recipes = decorate_recipe_list_with_sources(
            Recipe.objects.filter(id__in=matched_ids).distinct()
        ).order_by('sort_name')

        if not has_session:
            ingredient_recipes = ingredient_recipes.filter(is_public=True)

        return {
            'recipe_titles_res': [],
            'recipe_ingredients_res': list(ingredient_recipes),
            'ingredient_res': [],
            'no_results': len(ingredient_recipes) == 0,
        }
