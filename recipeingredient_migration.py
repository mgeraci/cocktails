from cocktails_app.models import IngredientStep

for i in IngredientStep.objects.all():
    i.ingredient_foo = i.ingredient
    i.amount_num_foo = i.amount_num
    i.amount_den_foo = i.amount_den
    i.unit_foo = i.unit

    i.save()
