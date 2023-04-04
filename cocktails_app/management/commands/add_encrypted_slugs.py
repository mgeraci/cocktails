from django.core.management.base import BaseCommand, CommandError
from cocktails_app.models import Recipe
from cocktails_app.sharing import encrypt

class Command(BaseCommand):
    help = "Generates encrypted slugs for all recipes; use only with a pre-3.8 version of Python."

    def handle(self, *args, **options):
        self.stdout.write("Generating encrypted slugs for all recipes...")
        for recipe in Recipe.objects.all():
            self.stdout.write(recipe.slug)
            self.stdout.write(encrypt(recipe.slug))
            recipe.encrypted_slug = encrypt(recipe.slug)
            recipe.save()
            self.stdout.write("wrote encryped_slug for %s" % recipe.slug)
