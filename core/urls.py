from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('home/', views.index, name='home'),  # Adiciona o nome 'home' para a mesma view
    path('contato', views.contato, name='contato'),
    path('produto/<int:pk>', views.produto, name='produto'),
    path('produto/detalhe/<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.logar_usuario, name='login'),
    path('logout/', views.deslogar_usuario, name='logout'),
    path('avaliacoes/', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('remover_do_carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
]

