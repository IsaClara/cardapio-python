from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AlimentoCardapio, Categoria, Cliente, Pedido, ItemPedidos

def index(request):
    # --- PROCESSAMENTO DO PEDIDO (POST) ---
    if request.method == 'POST':
        alimento_id = request.POST.get('alimento_id')
        nome_cliente = request.POST.get('nome_cliente')
        telefone = request.POST.get('telefone')
        quantidade = int(request.POST.get('quantidade', 1))

        alimento = get_object_or_404(AlimentoCardapio, id=alimento_id)

        #Validação de estoque preventiva
        if quantidade > alimento.disponivel_estoque:
            messages.error(request, f"Desculpe, só temos {alimento.disponivel_estoque} unidades disponíveis.")
            return redirect('cardapio:index')

        #Cria ou recupera o cliente
        cliente, criado = Cliente.objects.get_or_create(
            nome_cliente=nome_cliente,
            defaults={'telefone': telefone}
        )

        #Registra o Pedido
        pedido = Pedido.objects.create(cliente=cliente)

        #Salva o item vendido com o nome ItemPedidos
        ItemPedidos.objects.create(
            pedido=pedido,
            alimento=alimento,
            quantidade=quantidade,
            preco_unitario=alimento.preco
        )

        # Atualiza o estoque do estabelecimento
        alimento.disponivel_estoque -= quantidade
        if alimento.disponivel_estoque == 0:
            alimento.disponivel = False
        alimento.save()

        messages.success(request, f"Pedido n {pedido.id} realizado com sucesso")
        return redirect('cardapio:index')

    #LISTAGEM, FILTROS E PARÂMETRO DO MODAL E MÉTODO (GET) 
    busca = request.GET.get('g', '').strip()
    pegar_pedido = request.GET.get('pegar_pedido', '').strip()
    
    categorias = Categoria.objects.all()
    alimento_selecionado = None

    if busca and busca.isdigit():
        categoria_id = int(busca)
        cardapio = AlimentoCardapio.objects.filter(disponivel=True, categoria_id=categoria_id).order_by('nome_alimento')
    else:
        cardapio = AlimentoCardapio.objects.filter(disponivel=True).order_by('nome_alimento')[:20]

    if pegar_pedido and pegar_pedido.isdigit():
        alimento_selecionado = get_object_or_404(AlimentoCardapio, id=int(pegar_pedido))

    context = {
        'mensagem': 'Filtrado por Categoria' if busca else 'Seja bem-vindo ao cardápio',
        'categorias': categorias,
        'cardapio': cardapio,
        'busca_atual': busca,
        'alimento_selecionado': alimento_selecionado,
    }
    
    return render(request, 'Post/index.html', context)

def sobre(request):
    from django.http import HttpResponse
    return HttpResponse('<h1>Você está na página de sobre</h1>')

def contato(request):
    from django.http import HttpResponse
    return HttpResponse('O seu email é: teste@gmail.com')
