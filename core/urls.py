from django.urls import path
from .views import index, contato, produto, registrar_usuario, logar_usuario, deslogar_usuario

urlpatterns = [
    path('', index, name='index'),
    path('contato', contato, name='contato'),
    path('produto/<int:pk>', produto, name='produto'),
    path('registro/', registrar_usuario, name='registro'),
    path('login/', logar_usuario, name='login'),
    path('logout/', deslogar_usuario, name='logout'),
]
