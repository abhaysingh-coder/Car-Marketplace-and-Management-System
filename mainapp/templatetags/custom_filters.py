from django import template

register = template.Library()

@register.filter
def prettify(value):
    return str(value).replace('_', ' ').title()