from django.shortcuts import render
from django.http import HttpResponse

#http://127.0.0.1:8000/cardapio/
def index(request):
    return render(request, 'Post/index.html')
# Create your views here.

#http://127.0.0.1:8000/cardapio/sobre
def sobre(request):
    return HttpResponse('<h1>Você está na página de views</h1>')

#http://127.0.0.1:8000/cardapio/contato
def contato(request):
    return HttpResponse('O seu email é: teste@gmail.com /n e a sua senha é: 12391893')
