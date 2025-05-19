from django.shortcuts import render, redirect, get_object_or_404 # type: ignore

from core.models import Produto
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import models
from core.models import Pedido, ItemPedido, Avaliacao



def index(request):
    produtos = Produto.objects.all()
    context = {
        'curso': "Web progamming with Django Framework",
        'other': "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.",
        'other2': "Projeto de site de vendas com Django em andamento, por favor, aguarde...",
        'produtos' : produtos
    }
    return render(request, 'core/index.html' , context)

def contato(request):
    return render(request, 'core/contato.html')

def produto(request, pk):
    try:
        prod = Produto.objects.get(id=pk)
        context = {
            'produto': prod
        }
        return render(request, 'core/produto.html', context)
    except Produto.DoesNotExist:
        # Renderiza uma página fictícia para produtos inexistentes
        return render(request, 'core/produto_nao_encontrado.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Conta criada com sucesso para {username}!')
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'core/registrar_usuario.html', {'form': form})

def logar_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def deslogar_usuario(request):
    logout(request)
    return redirect('index')

def listar_pedidos(request):
    # Consulta otimizada com select_related para buscar os clientes relacionados
    pedidos = Pedido.objects.com_cliente()
    return render(request, 'core/listar_pedidos.html', {'pedidos': pedidos})

def listar_itens_pedido(request):
    # Consulta otimizada com select_related para buscar pedidos e produtos relacionados
    itens = ItemPedido.objects.com_relacionados()
    return render(request, 'core/listar_itens_pedido.html', {'itens': itens})

def listar_avaliacoes(request):
    query = request.GET.get('q')  # Obtém o termo de pesquisa do formulário
    if query:
        # Filtra as avaliações pelo nome do cliente ou do produto
        avaliacoes = Avaliacao.objects.com_relacionados().filter(
            models.Q(cliente__nome__icontains=query) | models.Q(produto__nome__icontains=query)
        )
    else:
        # Retorna todas as avaliações se não houver pesquisa
        avaliacoes = Avaliacao.objects.com_relacionados()
    return render(request, 'core/listar_avaliacoes.html', {'avaliacoes': avaliacoes})