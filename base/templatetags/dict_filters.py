# base/templatetags/dict_filters.py
from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """
    Permite acessar uma chave de dicionário no template.
    Exemplo: dicionario|dict_get:'chave'
    """
    return d.get(key)
