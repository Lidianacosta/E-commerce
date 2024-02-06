from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from produto.models import Variacao
from utils import utils

from .models import Pedido, ItemPedido

PER_PAGE = 5

# Create your views here.


class DispatchLoginMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Você precisa fazer login.")
            return redirect('perfil:criar')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        pedido = super().get_queryset(*args, **kwargs)
        pedido = pedido.filter(user=self.request.user)
        return pedido


class PagarView(DispatchLoginMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido


class FecharPedidoView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Você precisa fazer login.")
            return redirect('perfil:criar')

        carrinho = self.request.session.get('carrinho')

        if not carrinho:
            messages.warning(self.request, "Carrinho vazio.")
            return redirect('produto:lista')

        carrinho_variacao_ids = [k for k in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        alteracao_quantidade = False

        for variacao in bd_variacoes:
            variacao_id = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[variacao_id]['quantidade']
            preco_unitario = carrinho[variacao_id]['preco_unitario']
            preco_unitario_promocional = (
                carrinho[variacao_id]['preco_unitario_promocional']
            )

            if qtd_carrinho > estoque:
                carrinho[variacao_id]['quantidade'] = estoque
                carrinho[variacao_id]['preco_quantitativo'] = (
                    estoque * preco_unitario
                )
                carrinho[variacao_id]['preco_quantitativo_promocional'] = (
                    estoque * preco_unitario_promocional
                )
                alteracao_quantidade = True

        if alteracao_quantidade:
            self.request.session.save()
            messages.warning(
                self.request,
                'Estoque insuficiente para alguns produtos do seu carrinho. '
                'Reduzimos a quantidade desses produtos. Por favor, Verifique '
                'quais produtos foram afetados a seguir.'
            )
            return redirect(self.request, 'produto:carrinho')

        qtd_total_carrinho = utils.carrinho_quantidade_total(carrinho)
        valor_total_carrinho = utils.carrinho_total(carrinho)

        pedido = Pedido(
            user=self.request.user,
            quantidade_total=qtd_total_carrinho,
            total=valor_total_carrinho,
            status='C'
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto_nome=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao_nome=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        self.request.session['carrinho'] = {}
        self.request.session.save()

        return redirect(reverse('pedido:pagar', kwargs={'pk': pedido.pk}))


class DetalheView(DispatchLoginMixin, DetailView):
    model = Pedido
    template_name = 'pedido/detalhe.html'


class ListaView(DispatchLoginMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = PER_PAGE
    ordering = '-id'
