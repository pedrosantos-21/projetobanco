from django.contrib import admin

from .models import Produto, Client # Importa o modelo Produto
 
class produtoAdmin(admin.ModelAdmin): # Cria uma classe para o modelo Produto, que herda de admin.ModelAdmin
    list_display = ('nome', 'preco', 'estoque') # Exibe os campos nome, preco e estoque

class clienteAdmin(admin.ModelAdmin): # Cria uma classe para o modelo Client, que herda de admin.ModelAdmin
    list_display = ('nome', 'sobre_nome', 'email', 'data_nascimento') # Exibe os campos nome, sobrenome e email

admin.site.register(Produto, produtoAdmin) # Registra o modelo Produto
admin.site.register(Client, clienteAdmin) # Registra o modelo Client
