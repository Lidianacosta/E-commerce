from django.template import Library
from utils.formata_preco import formata_preco as formatar

register = Library()


@register.filter
def formata_preco(num):
    return formatar(num)
