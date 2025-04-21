from django.contrib import admin

from .models import Produto, Client, Categoria, Pedido, ItemPedido, Avaliacao

class ProdutoAdmin(admin.ModelAdmin): 
    list_display = ('nome', 'preco', 'estoque') 

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobre_nome', 'email', 'data_nascimento') 

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')  # Ajuste os campos conforme o modelo Categoria

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido')  # Ajuste os campos conforme o modelo Pedido

class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade')  # Ajuste os campos conforme o modelo ItemPedido

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'cliente', 'nota', 'comentario', 'data')  # Ajuste os campos conforme o modelo Avaliacao

admin.site.register(Produto, ProdutoAdmin) 
admin.site.register(Client, ClienteAdmin) 
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)