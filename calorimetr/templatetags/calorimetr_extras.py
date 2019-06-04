from django import template

register = template.Library()

@register.filter
def calorie(portions,_eating):
    return portions.filter(eating=_eating)[0].val
