from django import forms
from .models import Product
from core.forms import RequiredFieldsMixin

class ProductForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'unit_price', 'medida_x', 'medida_y', 'description']
        widgets = {
            # --- CAMPO DE CÓDIGO ATUALIZADO ---
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly', # Torna o campo não editável
                'placeholder': '(Automático)' # Informa o usuário
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_x': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_y': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # --- LÓGICA ADICIONADA ---
        # Torna o campo de código não obrigatório no formulário
        self.fields['code'].required = False