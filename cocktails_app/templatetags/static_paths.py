import os
import json
from django import template
from django.template.defaultfilters import stringfilter
from cocktails_app.utils import get_static_path

register = template.Library()

@register.filter
@stringfilter
def get_static_filname(file):
    return get_static_path(file);
