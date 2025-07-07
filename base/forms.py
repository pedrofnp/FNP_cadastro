from django import forms
from django.forms import inlineformset_factory
from .models import Contato, Interesse, Email, Telephone 



class ContactForm(forms.ModelForm, forms.Form):
        interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all(),  # Puxa todos os interesses do banco de dados
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),  # Lista suspensa múltipla
        required=False  # Campo não obrigatório
        )
        class Meta:
            model = Contato
            fields = ['nome',  'cargo', 'entidade', 'partido' ,'interesses' , 'estado', 'municipio', 'observacoes', 'foto']
            """ fields = '__all__' """

            widgets = {
                'nome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o nome do contato'}),
                'cargo': forms.Select(attrs={'class': 'form-control','id': 'cargo'}),
                'entidade': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Instituição'}),
                'partido': forms.Select(attrs={'class': 'form-control','id': 'partido'}),  # Certifique-se de que o ID seja "estado"
                'estado': forms.Select(attrs={'class': 'form-control','id': 'estado'}),  # Certifique-se de que o ID seja "estado"
                'municipio': forms.Select(attrs={'class': 'form-control','id': 'municipio'}),  # Certifique-se de que o ID seja "municipio"
                'observacoes': forms.Textarea(attrs={'class': "form-control", 'id':"observacoes", 'rows':2}),
                'foto': forms.FileInput(attrs={'class': "form-control", 'id':"observacoes",'accept':"image/*"})

            }

# Create inline formsets for Email and Telefone
EmailFormSet = inlineformset_factory(Contato, Email, fields=['email'], extra=1, can_delete=True)
TelephoneFormSet = inlineformset_factory(Contato, Telephone, fields=['telephone'], extra=1, can_delete=True)