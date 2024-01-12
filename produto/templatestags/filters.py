from django.template import Library
from utils.utils import formata_preco as formatar
from utils.utils import carrinho_quantidade_total, carrinho_total

register = Library()


@register.filter
def formata_preco(num):
    return formatar(num)


@register.filter('carrinho_quantidade_total')
def carrinho_qtd_total(carrinho):
    return carrinho_quantidade_total(carrinho)


@register.filter('carrinho_total')
def carrinho_preco_total(carrinho):
    return carrinho_total(carrinho)
