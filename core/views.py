from django.shortcuts import render, redirect, get_object_or_404 # type: ignore

from core.models import Produto
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import models
from core.models import Pedido, ItemPedido, Avaliacao
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(ListView):
    model = Produto
    template_name = 'core/index.html'
    context_object_name = 'produtos'


class ContatoView(TemplateView):
    template_name = 'core/contato.html'

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'core/produto.html'
    context_object_name = 'produto'

class DetalheProdutoView(DetailView):
    model = Produto
    template_name = 'core/detalhe_produto.html'
    context_object_name = 'produto'

class RegistrarUsuarioView(FormView):
    template_name = 'core/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ListarPedidosView(ListView):
    model = Pedido
    template_name = 'core/listar_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Pedido.objects.com_cliente()

class ListarItensPedidoView(ListView):
    model = ItemPedido
    template_name = 'core/listar_itens_pedido.html'
    context_object_name = 'itens'

    def get_queryset(self):
        return ItemPedido.objects.com_relacionados()

class ListarAvaliacoesView(ListView):
    model = Avaliacao
    template_name = 'core/listar_avaliacoes.html'
    context_object_name = 'avaliacoes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Avaliacao.objects.com_relacionados().filter(
                models.Q(cliente__nome__icontains=query) | models.Q(produto__nome__icontains=query)
            )
        return Avaliacao.objects.com_relacionados()

class LogarUsuarioView(LoginView):
    template_name = 'core/login.html'

class DeslogarUsuarioView(LogoutView):
    next_page = 'index'


def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    try:
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade <= 0:
            raise ValueError
    except (ValueError, TypeError):
        messages.error(request, 'Quantidade inválida.')
        return redirect('detalhe_produto', pk=produto_id) # Redireciona de volta para a página do produto

    carrinho = request.session.get('carrinho', {}) # Inicializa ou acessa o carrinho na sessão

    produto_id_str = str(produto.id)

    if produto_id_str in carrinho:
        carrinho[produto_id_str] += quantidade
    else:
        carrinho[produto_id_str] = quantidade

    if carrinho[produto_id_str] > produto.estoque:
        carrinho[produto_id_str] = produto.estoque 
        messages.warning(request, f'Não há {quantidade} unidades de "{produto.nome}" em estoque. Adicionamos o máximo disponível ({produto.estoque}).')
    else:
        messages.success(request, f'"{produto.nome}" adicionado ao carrinho!')

    request.session['carrinho'] = carrinho 
    request.session.modified = True 
    return redirect('index') 

def ver_carrinho(request):
    carrinho_session = request.session.get('carrinho', {}) # Renomeado para evitar conflito com 'carrinho' de fora
    itens_carrinho = []
    total_carrinho = 0

    for produto_id_str, quantidade in carrinho_session.items():
        # Lembre-se que produto_id_str é uma string, converta para int para buscar no DB
        produto = get_object_or_404(Produto, pk=int(produto_id_str))
        subtotal = produto.preco * quantidade
        total_carrinho += subtotal
        itens_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
    
    context = {
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho
    }
    return render(request, 'core/carrinho.html', context)

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id) # Garante que a chave é string

    if produto_id_str in carrinho:
        del carrinho[produto_id_str] # Remove o item do dicionário
        request.session['carrinho'] = carrinho # Salva o carrinho atualizado
        request.session.modified = True # Sinaliza modificação
        messages.info(request, 'Item removido do carrinho.')
    return redirect('ver_carrinho') # Redireciona para a página do carrinho
