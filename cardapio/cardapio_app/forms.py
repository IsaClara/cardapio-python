from django import forms
from django.core.exceptions import ValidationError
from . models import Cliente
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente','telefone']


    def clean_nome_cliente(self):
        nome = self.cleaned_data['nome_cliente']

        #caso o nome seja menor que 3 letras
        if len(nome) < 3:
            raise ValidationError('O nome deve ser maior que 3 letras')
        
        # serve para caso o cliente digite números, o regex(vulgo "^[A-Za-z ]+$", serve para permitir os nomes de A a Z, maiusculos ou minusculos com acentos ou não)
        if not re.match(r'^[A-Za-zÀ-ÿ ]+$', nome):
            raise ValidationError("Não digite números no nome.")
        
        return nome
        

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']

        telefone = telefone.replace(' ', '').replace('-', '')
        
        if len(telefone) <=11:
            raise ValidationError('O número deve possuir 11 digitos')
        
        if not telefone.isdigit():
            raise ValidationError('O telefone deve conter somente números ')
        
        return telefone
#preciso validar o nome e numero depois