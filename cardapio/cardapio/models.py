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
    disponivel_estoque = models.PositiveIntegerField('Estoque disponivel:', default=0)

    #relacionamentos

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
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

# Create your models here.
