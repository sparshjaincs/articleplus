from django import template

register = template.Library()

@register.filter
def replace(value):
    return value.replace(" ","_")

@register.filter
def split(value,field):
    return value.split(field)