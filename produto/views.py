from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, View, DetailView
from django.contrib import messages
from .models import Produto, Variacao
# Create your views here.

PER_PAGE = 9


class ListaProdutoListView(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = PER_PAGE
    ordering = 'nome'


class DetalheProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'


class AdicionarAoCarrinhoView(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:lista')
        )

        variacao_id = self.request.GET.get('vid', None)

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, pk=variacao_id)

        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session.get('carrinho')

        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        produto = variacao.produto
        imagem = produto.imagem.url if produto.imagem else ''

        if variacao_id in carrinho:  # type:ignore
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao.estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x do '
                    f'produto "{variacao.produto.nome}". Adicionamos {variacao.estoque} '
                    f'ao seu carrinho'
                )
                quantidade_carrinho = variacao.estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                "produto_id": produto.pk,
                'produto_nome': produto.nome,
                'variacao_nome': variacao.nome or '',
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': produto.slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(
            self.request,
            f'Produto {produto.nome} - {variacao.nome}'
            ' adicionado ao seu carrinho'
            f'{carrinho[variacao_id]["quantidade"]}x'
            if variacao.nome
            else f'Produto {produto.nome}'
            ' adicionado ao seu carrinho '
            f'{carrinho[variacao_id]["quantidade"]}x'

        )

        return redirect(http_referer)


class RemoverDoCarrinhoView(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:lista')
        )

        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            return redirect(http_referer)

        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            return redirect(http_referer)

        if variacao_id not in carrinho:
            return redirect(http_referer)

        messages.success(
            self.request,
            f'Poduto {carrinho[variacao_id]["produto_nome"]}'
            f' - {carrinho[variacao_id]["variacao_nome"]} removido do seu carrinho'
            if carrinho[variacao_id]["variacao_nome"]
            else f'Poduto {carrinho[variacao_id]["produto_nome"]} removido do seu carrinho'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class CarrinhoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'produto/carrinho.html')


class ResumoDaCompra(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('perfil:criar')

        context = {
            'usuario': request.user,
        }
        return render(request, 'produto/resumo_da_compra.html', context)
