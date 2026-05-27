from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import AlimentoCardapio,Categoria
#http://127.0.0.1:8000/cardapio/
#onde acontece a criação do card do alimento
def index(request):
    categorias = Categoria.objects.all()
    cardapio = AlimentoCardapio.objects.filter(disponivel=True).order_by('nome_alimento')[:20]

    context={'mensagem':'Seja bem vindo ao cardapio',
             'categorias': categorias,
              'cardapio': cardapio}
    
    return render(request, 'Post/index.html', context)


#vai filtrar por ID
def filtroCategoria(request):
    busca = request.GET.get('g', '').strip()
    categorias = Categoria.objects.all()

    # Se escolheu uma categoria específica
    if busca and busca.isdigit():

        categoria_id = int(busca)
        # Filtra estritamente os alimentos da categoria selecionada
        cardapio = AlimentoCardapio.objects.filter(disponivel=True, categoria_id=categoria_id).order_by('nome_alimento')
    else:
        # Se escolheu "Todos os Produtos" (vazio), mostra tudo de novo
        cardapio = AlimentoCardapio.objects.filter(disponivel=True).order_by('nome_alimento')[:20]

    context = {
        'mensagem': 'Filtrado por Categoria',
        'categorias': categorias,
        'cardapio': cardapio,
        'busca_atual': busca, # Mantém o select marcado com a opção escolhida
    }
    return render(request, 'Post/index.html', context)

# para registrar todos os alimentos e mandar para a tela de pedidos
def telaPedido(request):
    pegar_pedido = request.GET.get('id')
    alimento_id= get_object_or_404(AlimentoCardapio,id=alimento_id)
    context ={
        'alimento': alimento_id
    }

    return render(request, 'Post/index.html', context)

#http://127.0.0.1:8000/cardapio/sobre
def sobre(request):
    return HttpResponse('<h1>Você está na página de views</h1>')

#http://127.0.0.1:8000/cardapio/contato
def contato(request):
    return HttpResponse('O seu email é: teste@gmail.com /n e a sua senha é: 12391893')
