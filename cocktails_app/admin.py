from django.contrib import admin
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    IngredientStep,
    Unit,
    Source,
    Glass,
)


class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientCategoryAdmin(admin.ModelAdmin):
    pass


class IngredientStepInline(admin.TabularInline):
    model = IngredientStep


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientStepInline,
    ]


class UnitAdmin(admin.ModelAdmin):
    pass


class SourceAdmin(admin.ModelAdmin):
    pass


class GlassAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Glass, GlassAdmin)
