from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutoListView.as_view(), name='lista'),
    path('detalhe/<slug:slug>/',
         views.DetalheProdutoDetailView.as_view(), name='detalhe'),
    path('adicionar-ao-carrinho/', views.AdicionarAoCarrinhoView.as_view(),
         name='adicionar_ao_carrinho'),
    path('remover-do-carrinho/', views.RemoverDoCarrinhoView.as_view(),
         name='remover_do_carrinho'),
    path('carrinho/', views.CarrinhoView.as_view(), name='carrinho'),
    path('finalizar/', views.FinalizarView.as_view(), name='finalizar'),

]
