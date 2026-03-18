from django import forms
from example.models import User, TagProblema

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