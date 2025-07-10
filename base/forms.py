from django import forms
from django.forms import inlineformset_factory
from .models import Contato, Interesse, Email, Telephone

class ContactForm(forms.ModelForm):
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        help_text='',
        label='Áreas de Interesse'
    )

    class Meta:
        model = Contato
        fields = [
            'nome', 'cargo', 'entidade', 'partido', 'interesses',
            'estado', 'municipio', 'observacoes', 'foto'
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do contato'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control',
                'id': 'cargo'
            }),
            'entidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instituição'
            }),
            'partido': forms.Select(attrs={
                'class': 'form-control',
                'id': 'partido'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
                'id': 'estado'
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-control',
                'id': 'municipio'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': "form-control",
                'id': "observacoes",
                'rows': 2
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'accept': "image/*"
            }),
        }

# Formsets para cadastro e edição de e-mails e telefones
EmailFormSet = inlineformset_factory(
    Contato, Email,
    fields=['email'],
    extra=1,
    can_delete=True,
    widgets={'email': forms.EmailInput(attrs={'class': 'form-control'})}
)

TelephoneFormSet = inlineformset_factory(
    Contato, Telephone,
    fields=['telephone'],
    extra=1,
    can_delete=True,
    widgets={'telephone': forms.TextInput(attrs={'class': 'form-control'})}
)
