from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def active_menu_item(x, y):
    print 'active menu item func'
    print x, y

    try:
	return str(x).index(str(y)) > -1

    except Exception:
        return False
