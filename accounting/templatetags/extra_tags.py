from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='time_diff')
def time_diff(value, arg):
    delta = value - arg
    return delta.days

@register.filter(name='min_diff')
def min_diff(value, arg):
    delta = value - arg
    return delta.total_seconds()/60