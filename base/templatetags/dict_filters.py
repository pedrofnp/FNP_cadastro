from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Permite acessar dicionários no template com chave dinâmica."""
    return d.get(key, {})
