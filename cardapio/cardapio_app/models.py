from django.db import models
from django.urls import reverse



class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    

class AlimentoCardapio(models.Model):
    nome_alimento = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(max_length=250)
    foto_alimento = models.ImageField('foto', upload_to='fotoalimento/', blank=True, null=True)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2,default=0)
    disponivel= models.BooleanField('Disponivel', default=True)

    #relacionamentos

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='Alimentos',
        verbose_name='Categoria',
    )

    class Meta:
        verbose_name = 'AlimentoCardapio'
        verbose_name_plural = 'AlimentosCardapio'
        ordering = ['nome_alimento']

    def __str__(self):
        return self.nome_alimento

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=50)
    telefone = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome_cliente']

    def __str__(self):
        return self.nome_cliente
    
class Pedido(models.Model):
    # Opções de status para a comanda
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Preparando', 'Preparando'),
        ('Concluído', 'Concluído'),
    ]

    cliente = models.ForeignKey(
    Cliente,
    on_delete=models.CASCADE,
    related_name='Pedidos')

    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pendente',
        verbose_name='Status do Pedido'
    )
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.cliente} - {self.criado_em}'
    
    def total(self):
        return sum(item.quantidade * item.preco_unitario for item in self.Itens.all())
    

class ItemPedidos(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='Itens')
    
    alimento = models.ForeignKey(
        AlimentoCardapio,
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField(
        default=1)
    
    preco_unitario = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.pedido.id} - {self.alimento.nome_alimento}' 
