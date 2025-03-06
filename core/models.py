from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255) #"Nome", é a label do atributo nome
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2)
    estoque = models.IntegerField("Quantidade em estoque")
    descricao = models.TextField()

    def __str__(self):#método que retorna o nome do produto
        return f'{self.nome}'

class Client(models.Model):
    nome = models.CharField("Nome", max_length=100)
    sobre_nome = models.CharField("Sobrenome", max_length=100)
    email = models.EmailField("Email", max_length=100)
    cpf = models.CharField("CPF", max_length=11)
    data_nascimento = models.DateField("Data de nascimento")
    endereco = models.CharField("Endereço", max_length=200)
    telefone = models.CharField("Telefone", max_length=11)
    
    def __str__(self):
        return f'{self.nome} {self.sobre_nome} {self.cpf}'