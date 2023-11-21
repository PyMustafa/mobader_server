from django import template

register = template.Library()

@register.filter
def remove_en(value):
    return value.replace("/en", "")

@register.filter
def add_en(value):
    return "/en" + value