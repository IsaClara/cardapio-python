from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cardapio'

urlpatterns = [
    # http://127.0.0
    # Esta rota agora controla a listagem, o filtro por ID e o Modal ao mesmo tempo!
    path('', views.index, name='index'),

    # http://127.0.0sobre
    path('sobre/', views.sobre, name='sobre'),

    # http://127.0.0contato
    path('contato/', views.contato, name='contato'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
