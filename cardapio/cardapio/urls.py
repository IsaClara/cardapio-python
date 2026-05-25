from django.urls import path
from . import views

app_name = 'cardapio'

urlpatterns = [
    #http://127.0.0.1:8000/cardapio/
    path('', views.index, name='index'),

    #http://127.0.0.1:8000/cardapio/sobre
    path('sobre', views.sobre, name='sobre'),
    #http://127.0.0.1:8000/cardapio/contato
    path('contato', views.contato, name='contato'),
]

