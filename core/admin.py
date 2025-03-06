from django.contrib import admin

from .models import Produto, Client 
 
class produtoAdmin(admin.ModelAdmin): 
    list_display = ('nome', 'preco', 'estoque') 

class clienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobre_nome', 'email', 'data_nascimento') 

admin.site.register(Produto, produtoAdmin) 
admin.site.register(Client, clienteAdmin) 
