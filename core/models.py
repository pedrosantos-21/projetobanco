from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255) 
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2)
    estoque = models.IntegerField("Quantidade em estoque")
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
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

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField("Descrição", blank=True, null=True)

    def __str__(self):
        return self.nome

class PedidoManager(models.Manager):
    def com_cliente(self):
        return self.select_related('cliente')

class Pedido(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)

    objects = PedidoManager()

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome}'

class ItemPedidoManager(models.Manager):
    def com_relacionados(self):
        return self.select_related('pedido', 'produto')

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    objects = ItemPedidoManager()

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

class AvaliacaoManager(models.Manager):
    def com_relacionados(self):
        return self.select_related('cliente', 'produto')

class Avaliacao(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    comentario = models.TextField()
    nota = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    objects = AvaliacaoManager()

    def __str__(self):
        return f'Avaliação de {self.cliente.nome} - Nota {self.nota}'