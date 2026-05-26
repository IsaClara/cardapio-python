from django.contrib import admin
from .models import Categoria,Cliente,AlimentoCardapio

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
    list_display=('nome_alimento','descricao','preco','foto_alimento','disponivel','disponivel_estoque',)
    search_fields=('nome_alimento','preco','categoria',)
    list_display_links=('descricao',)
    list_editable=('nome_alimento','preco','foto_alimento','disponivel','disponivel_estoque',)
    autocomplete_fields=('categoria',)
    fieldsets= (
        ('Informações principais:', {
            'fields': ('nome_alimento','descricao','foto_alimento',)
        }),
        ('Detalhes:', {
            'fields': ('preco','disponivel','disponivel_estoque',)
        }),
        ('Relacionamentos:', {
            'fields': ('categoria',)
        }),
        
    )
    list_per_page=30