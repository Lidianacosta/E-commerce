from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from .models import Produto
# Create your views here.

PER_PAGE = 9


class ListaProdutoListView(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = PER_PAGE


class DetalheProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'


class AdicionarAoCarrinhoView(View):
    pass


class RemoverDoCarrinhoView(View):
    pass


class CarrinhoView(View):
    pass


class FinalizarView(View):
    pass
