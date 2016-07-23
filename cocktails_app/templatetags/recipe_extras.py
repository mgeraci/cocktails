# -*- coding: utf-8 -*-

from django import template
import re

register = template.Library()


value_re = re.compile('\d+\.\d+')

def format_value(step):
    iterator = re.finditer(value_re, step)

    for match in iterator:
        num = match.group()
        (whole, fraction) = num.split('.')

        if whole == '0':
            step = step.replace('0', '')

        if fraction == '0':
            step = step.replace(num, whole)
        elif fraction == '25':
            step = step.replace('.25', u'¼')
        elif fraction == '33':
            step = step.replace('.33', u'⅓')
        elif fraction == '5':
            step = step.replace('.5', u'½')
        elif fraction == '66':
            step = step.replace('.66', u'⅔')
        elif fraction == '75':
            step = step.replace('.75', u'¾')

        if whole == '0' and fraction == '0':
            print step
            step = re.sub(r'^\. ', '', step)

    return step


register.filter('format_value', format_value)
