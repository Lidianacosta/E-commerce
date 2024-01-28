from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pedido(models.Model):
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    quantidade_total = models.PositiveIntegerField()
    status = models.CharField(
        max_length=1,
        default='A',
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        ),
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Items do Pedido"

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto_nome = models.CharField(max_length=100)
    produto_id = models.PositiveIntegerField()
    variacao_nome = models.CharField(max_length=100)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField(default=1)
    imagem = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f'Item do {self.pedido}'
