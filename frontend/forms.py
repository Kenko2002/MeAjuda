from django import forms
from example.models import User, TagProblema, Comunidade, Mensagem

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'bio', 'problemas']
        widgets = {
            'problemas': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deixa o visual do bootstrap nos checkboxes
        self.fields['problemas'].queryset = TagProblema.objects.all()


class ComunidadeForm(forms.ModelForm):
    class Meta:
        model = Comunidade
        fields = ['nome', 'descricao', 'anonima']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da comunidade'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição breve do grupo'}),
            'anonima': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva sua mensagem aqui...'
            }),
        }
        labels = {
            'texto': ''
        }