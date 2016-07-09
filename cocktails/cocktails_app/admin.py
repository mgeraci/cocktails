from django.contrib import admin
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    IngredientStep,
    ActionStep,
    Action,
    Unit,
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


class UnitAdmin(admin.ModelAdmin):
    pass


class ActionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Unit, UnitAdmin)
