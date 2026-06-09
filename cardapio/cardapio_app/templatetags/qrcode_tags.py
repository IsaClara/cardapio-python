import qrcode
import io
import base64
from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def generate_qr_code(context, view_name, *args, **kwargs):
    # 1. Pega a requisição atual para descobrir o domínio do site (ex: http://127.0.0.1:8000)
    request = context['request']
    
    # 2. Transforma a tag de URL do Django no caminho relativo (ex: /cardapio/)
    relative_url = reverse(view_name, args=args, kwargs=kwargs)
    
    # 3. Junta tudo para formar o link completo que o celular vai ler
    full_url = request.build_absolute_uri(relative_url)
    
    # 4. Gera o QR Code na memória (sem salvar arquivo no computador)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 5. Converte a imagem para Base64 (texto) para exibir direto na tag <img>
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{qr_base64}"
