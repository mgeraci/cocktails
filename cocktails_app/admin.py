from django.contrib import admin
from cocktails_app.utils import get_static_path
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    RecipeIngredient,
    Unit,
    Source,
    Glass,
    RecipeCategory,
    RecipeTag,
)


admin.ModelAdmin.list_per_page = 500


class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientCategoryAdmin(admin.ModelAdmin):
    pass


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient

    # the number of ingredient rows to show on a recipe admin page
    extra = 10


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeIngredientInline,
    ]

    def has_tag(self, obj):
        return obj.tags.exists()

    list_display = ('name', 'source', 'category', 'has_tag')

    class Media:
        css = {
            'all': ('dist/{}'.format(get_static_path('admin.css')),)
        }
        js = ('dist/{}'.format(get_static_path('admin.js')),)


class UnitAdmin(admin.ModelAdmin):
    pass


class SourceAdmin(admin.ModelAdmin):
    pass


class GlassAdmin(admin.ModelAdmin):
    pass


class RecipeCategoryAdmin(admin.ModelAdmin):
    pass


class RecipeTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Glass, GlassAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
