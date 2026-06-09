from django.contrib import admin
from .models import Categoria,Cliente,AlimentoCardapio,Pedido,ItemPedidos

# Register your models here.


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=('nome_cliente','telefone')
    search_fields=('nome_cliente',)

class AlimentoCardapioInLine(admin.TabularInline):
    model= AlimentoCardapio
    extra=0
    fields=('nome_alimento','preco','disponivel')
    show_change_link=True

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display=('nome',)
    search_fields=('nome',)
    inlines=[AlimentoCardapioInLine]


@admin.register(AlimentoCardapio)
class AlimentoCardapioAdmin(admin.ModelAdmin):
    list_display=('nome_alimento','descricao','preco','foto_alimento','disponivel',)
    search_fields=('nome_alimento','preco','categoria',)
    list_display_links=('descricao',)
    list_editable=('nome_alimento','preco','foto_alimento','disponivel',)
    autocomplete_fields=('categoria',)
    fieldsets= (
        ('Informações principais:', {
            'fields': ('nome_alimento','descricao','foto_alimento',)
        }),
        ('Detalhes:', {
            'fields': ('preco','disponivel',)
        }),
        ('Relacionamentos:', {
            'fields': ('categoria',)
        }),
        
    )
    list_per_page=30

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedidos
    extra = 0
    # deixado como 'modo leitura' pro dono nao alterar o pedido kkkkk
    readonly_fields = ('alimento', 'quantidade', 'preco_unitario') 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('cliente__nome_cliente',)
    inlines = [ItemPedidoInline] # Mostra os itens comprados dentro do pedido correspondente