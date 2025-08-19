from django import template

register = template.Library()

@register.filter
def my_filter(a,b):
    return zip(a, b)
