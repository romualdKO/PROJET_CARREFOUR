from django import template

register = template.Library()

@register.filter(name='sum_attr')
def sum_attr(queryset, attribute):
    """
    Somme d'un attribut d'un queryset ou d'une liste d'objets
    Usage: {{ transactions_session|sum_attr:"montant_final" }}
    """
    try:
        return sum(getattr(obj, attribute, 0) for obj in queryset)
    except (TypeError, ValueError, AttributeError):
        return 0
