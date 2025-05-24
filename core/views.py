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

def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'core/detalhe_produto.html', {'produto': produto})