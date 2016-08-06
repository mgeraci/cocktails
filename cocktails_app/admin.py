from django.contrib import admin
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    RecipeIngredient,
    Unit,
    Source,
    Glass,
)


class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientCategoryAdmin(admin.ModelAdmin):
    pass


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeIngredientInline,
    ]

    class Media:
        css = {
            'all': ('css/vendor/chosen.css',)
        }

        js = (
            'js/vendor/jquery-3.1.0.min.js',
            'js/vendor/chosen.jquery.min.js',
            'js/admin/recipe-admin.js',
        )


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
