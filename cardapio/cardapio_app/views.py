from django.shortcuts import render, get_object_or_404, redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AlimentoCardapio, Categoria, Cliente, Pedido, ItemPedidos
from django.contrib.auth import authenticate, login, logout

def index(request):
    busca = request.GET.get('g', '').strip()
    ver_carrinho = request.GET.get('ver_carrinho', '')

    categorias = Categoria.objects.all()

    if busca and busca.isdigit():
        cardapio = AlimentoCardapio.objects.filter(
            disponivel=True,
            categoria_id=int(busca)
        ).order_by('nome_alimento')
    else:
        cardapio = AlimentoCardapio.objects.filter(
            disponivel=True
        ).order_by('nome_alimento')[:20]

    # abrir modal
    abrir_modal_pedidos = (ver_carrinho == 'sim')

    # cliente logado (via session)
    cliente_id = request.session.get('cliente_id')

    itens_pedido = []
    if cliente_id:
        itens_pedido = ItemPedidos.objects.filter(
            pedido__cliente_id=cliente_id
        ).select_related('alimento', 'pedido')

    return render(request, 'Post/index.html', {
        'mensagem': 'Cardápio Digital',
        'categorias': categorias,
        'cardapio': cardapio,
        'busca_atual': busca,
        'abrir_modal_pedidos': abrir_modal_pedidos,
        'itens_pedido': itens_pedido,
    })



def criar_pedido(request):
    if request.method != 'POST':
        return redirect('cardapio_app:index')

    alimento_id = request.POST.get('alimento_id')
    nome_cliente = request.POST.get('nome_cliente', 'Visitante')
    quantidade = int(request.POST.get('quantidade', 1))

    alimento = get_object_or_404(AlimentoCardapio, id=alimento_id)

    # cliente
    cliente, _ = Cliente.objects.get_or_create(nome_cliente=nome_cliente)

    # salva cliente na sessão
    request.session['cliente_id'] = cliente.id

    # pega último pedido ou cria um
    pedido = Pedido.objects.filter(cliente=cliente).last()

    if not pedido:
        pedido = Pedido.objects.create(cliente=cliente)

    # cria item e quando clica no mesmo de novo, a quantidade é somada
    item, created = ItemPedidos.objects.get_or_create(
    pedido=pedido,
    alimento=alimento,
    defaults={
        'quantidade': quantidade,
        'preco_unitario': alimento.preco
    }
)

    if not created:
        item.quantidade += quantidade
        item.save()

    return redirect('cardapio_app:index')


def finalizar_pedido(request):
    if request.method != 'POST':
        return redirect('cardapio_app:index')

    cliente_id = request.session.get('cliente_id')
    nome_cliente = request.POST.get('nome_cliente', '').strip()

    if cliente_id and nome_cliente:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.nome_cliente = nome_cliente  # atualiza com o nome digitado
        cliente.save()

        # opcional: marcar pedido como finalizado
        Pedido.objects.filter(cliente=cliente).update()

        # limpa sessão
        request.session.pop('cliente_id', None)

    return redirect('cardapio_app:index')


def deletar_pedido(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemPedidos, id=item_id)
        item.delete()

    return redirect('cardapio_app:index')

#o login vai verificar se a conta admin ou uma conta criada no django admin existe pra poder ir pra parte do dashboard
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('cardapio_app:dashboard')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'post/login.html')

#vai dar logout caso clique no botao de sair no dashboard
def logout_view(request):
    logout(request)
    return redirect('cardapio_app:login')

@login_required
def dashboard_view(request):
    print("USER:", request.user)
    print("AUTH:", request.user.is_authenticated)

    categorias = Categoria.objects.all()
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
        'categorias': categorias,
        'categoria': list(categorias_mock),
        'comandas': comandas_mock,
    }
    return render(request, 'post/dashboard.html', context)