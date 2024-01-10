from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.PagarView.as_view(), name='pagar'),
    path('fechar-pedido/', views.FecharPedidoView.as_view(), name='fechar_pedido'),
    path('detalhe/<int:pk>', views.DetalheView.as_view(), name='detalhe'),
]
