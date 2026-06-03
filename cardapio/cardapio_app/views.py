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
    ver_carrinho = request.GET.get('ver_carrinho', '').strip()
    
    categorias = Categoria.objects.all()
    alimento_selecionado = None

    if busca and busca.isdigit():
        categoria_id = int(busca)
        cardapio = AlimentoCardapio.objects.filter(disponivel=True, categoria_id=categoria_id).order_by('nome_alimento')
    else:
        cardapio = AlimentoCardapio.objects.filter(disponivel=True).order_by('nome_alimento')[:20]

    abrir_modal_pedidos = False
    if ver_carrinho == 'sim':
        abrir_modal_pedidos = True

    


    context = {
        'mensagem': 'Bem-vindo!',
        'categorias': categorias,
        'cardapio': cardapio,
        'busca_atual': busca,
        'abrir_modal_pedidos': abrir_modal_pedidos, 
    }
    
    return render(request, 'Post/index.html', context)

def sobre(request):
    from django.http import HttpResponse
    return HttpResponse('<h1>Você está na página de sobre</h1>')

def contato(request):
    from django.http import HttpResponse
    return HttpResponse('O seu email é: teste@gmail.com')



# ISSO AQUI É SÓ DE TESTE

def login_view(request):
    # Se a pessoa enviar o formulário, redireciona direto pro dashboard (simulação)
    if request.method == 'POST':
        return redirect('cardapio_app:dashboard')
    return render(request, 'post/login.html')

def dashboard_view(request):
    # Dados fictícios para testar o front-end do painel do usuário
    categorias_mock = [
        {'id': 1, 'nome': 'Hambúrgueres', 'quantidade': 5},
        {'id': 2, 'nome': 'Bebidas', 'quantidade': 3},
        {'id': 3, 'nome': 'Pizzas', 'quantidade': 4},
    ]
    
    comandas_mock = [
        {
            'id': 101,
            'cliente': 'João Silva',
            'itens': '1x Pizza Brigadeiro, 1x Coca-Cola',
            'total': '27,00',
            'status': 'Pendente'
        },
        {
            'id': 102,
            'cliente': 'Maria Souza',
            'itens': '2x X-Burguer, 1x Batata Frita',
            'total': '54,00',
            'status': 'Preparando'
        }
    ]
    
    context = {
        'categorias': list(categorias_mock),
        'comandas': comandas_mock,
    }
    return render(request, 'post/dashboard.html', context)