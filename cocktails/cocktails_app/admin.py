from django.contrib import admin
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    IngredientStep,
    ActionStep,
    Action,
)


class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientCategoryAdmin(admin.ModelAdmin):
    pass


class IngredientStepInline(admin.TabularInline):
    model = IngredientStep


class ActionStepInline(admin.TabularInline):
    model = ActionStep


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        ActionStepInline,
        IngredientStepInline,
    ]


class ActionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Action, ActionAdmin)
