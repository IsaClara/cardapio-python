from django import forms
from django.core.exceptions import ValidationError
from . models import Cliente, Categoria, AlimentoCardapio
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente','telefone']


    def clean_nome_cliente(self):
        nome = self.cleaned_data['nome_cliente']

        if len(nome) < 3:
            raise ValidationError('O nome deve ser maior que 3 letras')
        
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

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Categoria'}),
        }

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = AlimentoCardapio
        fields = ['nome_alimento', 'descricao', 'foto_alimento', 'preco', 'disponivel', 'categoria']
        widgets = {
            'nome_alimento': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }


