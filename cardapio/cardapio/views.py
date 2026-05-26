from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import AlimentoCardapio
#http://127.0.0.1:8000/cardapio/
def index(request):
    cardapio = AlimentoCardapio.objects.filter(disponivel=True).order_by('nome_alimento')[:20]
    context={'mensagem':'Seja bem vindo ao cardapio', 'cardapio': cardapio}
    return render(request, 'Post/index.html', context)
# Create your views here.

#http://127.0.0.1:8000/cardapio/sobre
def sobre(request):
    return HttpResponse('<h1>Você está na página de views</h1>')

#http://127.0.0.1:8000/cardapio/contato
def contato(request):
    return HttpResponse('O seu email é: teste@gmail.com /n e a sua senha é: 12391893')
