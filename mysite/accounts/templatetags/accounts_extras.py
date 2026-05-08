from django import template

register = template.Library()

@register.filter
def tem_grupo(user, grupo):
    return user.is_authenticated and user.groups.filter(name=grupo).exists()