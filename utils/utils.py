def formata_preco(value):
    return f'R$ {value:.2f}'.replace('.', ',')


def carrinho_quantidade_total(carrinho):
    if not carrinho:
        return 0
    return sum([item.get('quantidade') for item in carrinho.values()])


def carrinho_total(carrinho):
    if not carrinho:
        return 0
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )
