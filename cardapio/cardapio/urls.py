from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cardapio'

urlpatterns = [
    #http://127.0.0.1:8000/cardapio/
    path('', views.index, name='index'),
    #vai filtrar a lista
    path('filtrar/', views.filtroCategoria, name='filtro_categoria'), # http://127.0.0filtrar/
    #http://127.0.0.1:8000/cardapio/sobre
    path('sobre/', views.sobre, name='sobre'),
    #http://127.0.0.1:8000/cardapio/contato
    path('contato/', views.contato, name='contato'),

    path('pedido/',views.telaPedido, name='pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)