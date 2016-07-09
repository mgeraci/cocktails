from django.contrib import admin
from cocktails_app.models import (
    Ingredient,
    IngredientCategory,
)

class IngredientAdmin(admin.ModelAdmin):
    pass

class IngredientCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientCategory, IngredientCategoryAdmin)
