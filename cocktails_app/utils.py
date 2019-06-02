from Crypto.Cipher import AES
import base64

from django.db.models import Count

from cocktails.localsettings import SHARE_KEY
from cocktails_app.models import Recipe


def encrypt(clear_text):
    enc_secret = AES.new(SHARE_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return cipher_text


def decrypt(cipher_text):
    dec_secret = AES.new(SHARE_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val


def get_recipes_with_duplicated_names(request):
    recipes = Recipe.get(request)
    recipes_with_duplicated_names = set(
        Recipe.objects.values('name').annotate(Count('id')).filter(id__count__gt=1).values_list('name', flat=True)
    )

    for recipe in recipes:
        if recipe.name in recipes_with_duplicated_names and recipe.source:
            recipe.name = u'{} ({})'.format(recipe.name, recipe.source)

    return recipes
