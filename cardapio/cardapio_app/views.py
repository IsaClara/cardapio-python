from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AlimentoCardapio, Categoria, Cliente, Pedido, ItemPedidos
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from groq import Groq
from django.conf import settings
from django.core.cache import cache
from .forms import CategoriaForm, AlimentoForm


client = Groq(api_key=settings.GROQ_API_KEY)

@login_required
@require_POST
def chat_view(request):
     
    #limitar o tamanho da frase
    msg = request.POST.get("message", "").strip()

    if not msg:
        return JsonResponse({"message": "Mensagem vazia"})

    if len(msg) > 300:
        return JsonResponse({"message": "Mensagem muito longa"}, status=400)
    
    #palavras proibidas
    blocked = ["senha", "hack", "exploit"]

    if any(word in msg.lower() for word in blocked):
        return JsonResponse({"message": "Não posso responder isso."})
    
    #LIMITE DE USUARIO POR ID
    cache_key = f"chat_limit_{request.user.id}_{request.META.get('REMOTE_ADDR')}"

    if cache.get(cache_key):
        return JsonResponse({"message": "Espere um pouco antes de enviar outra mensagem."}, status=429)

    cache.set(cache_key, True, timeout=2)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """

                Você é um assistente interno de um painel administrativo de restaurante.

                Sua função é APENAS ajudar o gerente a:
                - gerenciar comandas ativas
                - explicar como aceitar pedidos
                - explicar como marcar pedidos como "feito"
                - orientar uso do painel de dashboard

                Você NÃO pode responder sobre:
                - assuntos fora do sistema
                - programação
                - política
                - religião
                - qualquer tema externo

                Se o usuário perguntar algo fora do painel, responda:
                "Posso ajudar apenas com o gerenciamento do painel do restaurante."

                Você não executa ações sozinho.
                Você apenas orienta o usuário sobre o sistema.
                Respostas devem ser curtas e objetivas.

                O painel contém:
                - lista de comandas ativas
                - status: Pendente, Preparando, Concluído
                - botões: Aceitar Pedido, Marcar como Feito
                - categorias e itens do cardápio


                REGRAS OBRIGATÓRIAS:
                - Você NÃO executa ações.
                - Você NÃO altera pedidos.
                - Você NÃO acessa banco de dados.
                - Você NÃO confirma mudanças no sistema.
                Você APENAS explica o que o usuário deve fazer manualmente, você só pode responder em texto puro. Proibido JSON, código ou comandos.

                Responda sempre em texto simples.

                - Nunca responda com instruções automáticas de API ou código de execução.
                - Nunca diga que você "vai fazer" algo.
                - Sempre use linguagem como: "clique em", "vá até", "você pode".
                """
            },
            {
                "role": "user",
                "content": msg
            }
        ],
        temperature=0.3,
        max_completion_tokens=200,
    )

    return JsonResponse({
        "message": completion.choices[0].message.content
    })

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
    quantidade = int(request.POST.get('quantidade', 1))
    alimento = get_object_or_404(AlimentoCardapio, id=alimento_id)

    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = Cliente.objects.create(nome_cliente='Mesa/Visitante')
    else:
        cliente = Cliente.objects.create(nome_cliente='Mesa/Visitante')
        request.session['cliente_id'] = cliente.id

    # O status 'Carrinho' significa que o cliente ainda está escolhendo os itens
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, status='Carrinho')

    item, created = ItemPedidos.objects.get_or_create(
        pedido=pedido,
        alimento=alimento,
        defaults={'quantidade': quantidade, 'preco_unitario': alimento.preco}
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
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.nome_cliente = nome_cliente  # Atualiza o nome do cliente
            cliente.save()

            Pedido.objects.filter(cliente=cliente, status='Carrinho').update(status='Pendente')
            
            request.session.pop('cliente_id', None)
            
        except Cliente.DoesNotExist:
            pass

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

    return render(request, 'Post/login.html')

#vai dar logout caso clique no botao de sair no dashboard
def logout_view(request):
    logout(request)
    return redirect('cardapio_app:login')

@login_required
def dashboard_view(request):
    print("USER:", request.user)

    if request.method == 'POST':
        tipo_formulario = request.POST.get('tipo_formulario')

        if tipo_formulario == 'criar_categoria':
            nome_categoria = request.POST.get('nome_categoria', '').strip()
            if nome_categoria:
                Categoria.objects.get_or_create(nome=nome_categoria)
            return redirect('cardapio_app:dashboard')

        elif tipo_formulario == 'criar_alimento':
            categoria_id = request.POST.get('categoria_id')
            nome_alimento = request.POST.get('nome_alimento', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            preco = request.POST.get('preco', 0)


            foto_alimento = request.FILES.get('foto_alimento')

            if categoria_id and nome_alimento:
                categoria = get_object_or_404(Categoria, id=categoria_id)
                AlimentoCardapio.objects.create(
                    nome_alimento=nome_alimento,
                    descricao=descricao,
                    preco=preco,
                    categoria=categoria,
                    foto_alimento=foto_alimento,  
                    disponivel=True
                )
            return redirect('cardapio_app:dashboard')

    categorias = Categoria.objects.prefetch_related('Alimentos').all()
    comandas_ativas = Pedido.objects.filter(status='Pendente').prefetch_related('Itens__alimento').order_by('criado_em')

    context = {
        'categorias': categorias,
        'pedidos': comandas_ativas,
    }
    return render(request, 'Post/dashboard.html', context)


@login_required
def atualizar_status_pedido(request, pedido_id, novo_status):
    if request.method == "POST":
        pedido = get_object_or_404(Pedido, id=pedido_id)

        if novo_status == 'Concluído':
            pedido.delete()
        else:
            pedido.status = novo_status
            pedido.save()
            
            
    return redirect('cardapio_app:dashboard')

@login_required
def deletar_categoria_view(request, categoria_id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id=categoria_id)
        categoria.delete()
    return redirect('cardapio_app:dashboard')

@login_required
def deletar_alimento_view(request, alimento_id):
    if request.method == 'POST':
        alimento = get_object_or_404(AlimentoCardapio, id=alimento_id)
        alimento.delete()
    return redirect('cardapio_app:dashboard')
