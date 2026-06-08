from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cardapio_app'

urlpatterns = [
    # http://127.0.0
    # Esta rota agora controla a listagem, o filtro por ID e o Modal ao mesmo tempo!
    path('', views.index, name='index'),
    path('criar-pedido/', views.criar_pedido, name='criar_pedido'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('deletar-item/<int:item_id>/', views.deletar_pedido, name='deletar_pedido'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chat/', views.chat_view, name='chat')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
