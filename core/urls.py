from django.urls import path
from .views import (
    IndexView, ContatoView, ProdutoDetailView, DetalheProdutoView,
    RegistrarUsuarioView, ListarPedidosView, ListarItensPedidoView,
    ListarAvaliacoesView, LogarUsuarioView, DeslogarUsuarioView,
    adicionar_ao_carrinho, ver_carrinho, remover_do_carrinho
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', IndexView.as_view(), name='home'),
    path('contato', ContatoView.as_view(), name='contato'),
    path('produto/<int:pk>', ProdutoDetailView.as_view(), name='produto'),
    path('produto/detalhe/<int:pk>/', DetalheProdutoView.as_view(), name='detalhe_produto'),
    path('registro/', RegistrarUsuarioView.as_view(), name='registro'),
    path('pedidos/', ListarPedidosView.as_view(), name='listar_pedidos'),
    path('itens_pedido/', ListarItensPedidoView.as_view(), name='listar_itens_pedido'),
    path('avaliacoes/', ListarAvaliacoesView.as_view(), name='listar_avaliacoes'),
    path('login/', LogarUsuarioView.as_view(), name='login'),
    path('logout/', DeslogarUsuarioView.as_view(), name='logout'),
    path('adicionar_ao_carrinho/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('remover_do_carrinho/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
]

