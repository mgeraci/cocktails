from django import template

register = template.Library()

@register.filter
def active_menu_item(x, y):
    try:
        return str(x).index(str(y)) > -1

    except Exception:
        return False
